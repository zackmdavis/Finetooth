import os, sys
from datetime import datetime
from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from core.models import FinetoothUser, Post
from core.tests import factories as f


class SignupTest(TestCase):

    def test_can_sign_up(self):
        response = self.client.post(
            reverse('sign_up'),
            {'username': "signup_testr", 'password': "moeDukr(,rpdCesLlrqr",
             'email': "signuptest@example.com"}
        )
        # XX: The call to assertRedirects was printing an empty
        # dictionary to standard out (if someone accidentally left a
        # debugging print statement in Django core (?!), I couldn't
        # find it)
        with open(os.devnull, 'w') as dev_null:
            original_stdout = sys.stdout
            sys.stdout = dev_null
            self.assertRedirects(response, '/')
            sys.stdout = original_stdout
        self.assertTrue(
            FinetoothUser.objects.filter(username="signup_testr").exists()
        )

    @skip("an apparently spurious TransactionManagementError due to the issue "
          "described at http://stackoverflow.com/a/23326971")  # TODO FIXME
    def test_cannnot_claim_extant_username(self):
        f.FinetoothUserFactory.create(username="username_squatter")
        response = self.client.post(
            reverse('sign_up'),
            {'username': "username_squatter", 'password': "oclxJums^whyysmtam",
             'email': "metoo@example.com"},
            follow=True
        )
        self.assertIn(b"Username already exists.", response.content)


class TaggingTest(TestCase):

    def setUp(self):
        self.the_user = f.FinetoothUserFactory.create()
        self.other_user = f.FinetoothUserFactory.create()
        self.the_post = f.PostFactory.create(author=self.the_user)
        self.other_post = f.PostFactory.create()
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        self.extant_tag = f.TagFactory.create()
        self.the_post.tag_set.add(self.extant_tag)

    def test_user_can_tag_own_post(self):
        self.client.post(reverse('tag', args=(self.the_post.pk,)),
                         {'label': "taggable"})
        tags = self.the_post.tag_set
        self.assertTrue("taggable", tags.filter(label="taggable").exists())

    def test_user_cannot_tag_post_of_other(self):
        response = self.client.post(
            reverse('tag', args=(self.other_post.pk,)),
            {'label': "untaggable"}
        )
        self.assertEqual(403, response.status_code)
        tags = self.other_post.tag_set
        self.assertEqual(0, tags.count())

    def test_user_cannot_double_apply_same_tag(self):
        tags_before = self.the_post.tag_set.all()
        response = self.client.post(
            reverse('tag', args=(self.the_post.pk,)),
            {'label': self.extant_tag.label}
        )
        self.assertEqual(400, response.status_code)
        self.assertQuerysetEqual(
            self.the_post.tag_set.all(),
            [repr(t) for t in tags_before]
        )

class CommentingTest(TestCase):

    def setUp(self):
        self.the_user = f.FinetoothUserFactory.create()
        self.the_post = f.PostFactory.create()

    def test_can_submit_comment(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse("add_comment", args=(self.the_post.pk,)),
            {'content': "the way that we got that one cool shot"}
        )
        comment = self.the_post.comment_set.filter(commenter=self.the_user)[0]
        fragment_identifier = "#comment-{}".format(comment.pk)
        self.assertRedirects(
            response,
            reverse(
                "show_post",
                args=(self.the_post.year,
                      self.the_post.month,
                      self.the_post.slug)
            ) + fragment_identifier
        )

    def test_do_not_panic_on_blank_comment(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse("add_comment", args=(self.the_post.pk,)),
            {'content': ""}
        )
        self.assertNotEqual(500, response.status_code)


class BallotBoxTest(TestCase):

    def setUp(self):
        self.the_user = f.FinetoothUserFactory.create()
        self.the_post = f.PostFactory.create(content="hello Django world")

    def test_canot_vote_if_not_logged_in(self):
        response = self.client.post(
            reverse('vote', args=("post", self.the_post.pk)),
            {'startIndex': 1, 'endIndex': 5, 'value': 1}
        )
        self.assertEqual(response.status_code, 401)

    def test_cannot_submit_invalid_vote(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse('vote', args=("post", self.the_post.pk)),
            {'startIndex': 0,
             'endIndex': 5001,  # IndexError: string index out of range
             'value': 1}
        )
        self.assertEqual(response.status_code, 400)


class ProfileEditingTest(TestCase):

    def setUp(self):
        FinetoothUser.objects.create_user(
            username="Jennifer_Userton", password="vmR9*sdfp["
        )
        FinetoothUser.objects.create_user(
            username="Not_Jennifer", password="shsk$&hfio"
        )

    def test_can_edit_profile(self):
        self.client.login(username="Jennifer_Userton", password="vmR9*sdfp[")
        response = self.client.post(
            reverse('edit_profile', args=("Jennifer_Userton",)),
            {'url': "http://example.com/ju",
             'location': "Usertown, California"}
        )
        self.assertEqual(response.status_code, 302)
        the_user_transformed = FinetoothUser.objects.get(
            username="Jennifer_Userton"
        )
        self.assertEqual("http://example.com/ju",
                         the_user_transformed.url)
        self.assertEqual("Usertown, California",
                         the_user_transformed.location)

    def test_cannot_edit_profile_not_ones_own(self):
        self.client.login(username="Jennifer_Userton", password="vmR9*sdfp[")
        response = self.client.post(
            reverse('edit_profile', args=("Not_Jennifer",)),
            {'url': "http://example.com/ju",
             'location': "Usertown, California"}
        )
        self.assertEqual(403, response.status_code)


class PostTest(TestCase):

    def setUp(self):
        FinetoothUser.objects.create_user(
            username="Jennifer_Userton", password="vmR9*sdfp["
        )
        self.client.login(username="Jennifer_Userton", password="vmR9*sdfp[")

    def test_new_post(self):
        new_post_title = "A very entertaining post"
        response = self.client.post(
            reverse('new_post'),
            {'content': "Entertaining content!",
             'title': new_post_title,
             'slug': slugify(new_post_title)}
        )
        matching_posts = Post.objects.filter(
            content="Entertaining content!",
            title=new_post_title,
            slug=slugify(new_post_title)
        )
        self.assertEqual(len(matching_posts), 1)
