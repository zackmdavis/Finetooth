from datetime import datetime, timedelta

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from core.models import FinetoothUser, Post
from core.tests import factories as f
from core.tests.factories import romanize

class SignupTestCase(TestCase):

    def concerning_signup(self):
        response = self.client.post(
            reverse('sign_up'),
            {'username': "signup_testr",
             'password': "moeDukr(,rpdCesLlrq",
             'confirm_password': "moeDukr(,rpdCesLlrq",
             'email': "signuptest@example.com"}
        )
        self.assertRedirects(response, '/')
        user_queryset = FinetoothUser.objects.filter(username="signup_testr")
        self.assertTrue(user_queryset.exists())
        self.assertTrue(user_queryset[0].check_password("moeDukr(,rpdCesLlrq"))

    def concerning_the_inability_to_claim_extant_usernames(self):
        f.FinetoothUserFactory.create(username="username_squatter")
        response = self.client.post(
            reverse('sign_up'),
            {'username': "username_squatter",
             'password': "oclxJums^whyysmtam",
             'confirm_password': "oclxJums^whyysmtam",
             'email': "metoo@example.com"},
            follow=True
        )
        self.assertIn(b"A user with that username already exists.",
                      response.content)

    def concerning_confirm_passwords_needing_to_match(self):
        prior_user_count = FinetoothUser.objects.count()
        response = self.client.post(
            reverse('sign_up'),
            {'username': "pentest",
             'password': "*sd6f3mjdrt3y42",
             'confirm_password': "not_the_same_password_is_it",
             'email': "pt@example.com"},
            follow=True
        )
        post_user_count = FinetoothUser.objects.count()
        self.assertEqual(prior_user_count, post_user_count)
        self.assertEqual(422, response.status_code)

    def concerning_required_fields(self):
        prior_user_count = FinetoothUser.objects.count()
        response = self.client.post(
            reverse('sign_up'),
            {'username': '',
             'password': "oclxJums^whyysmtam",
             'confirm_password': "oclxJums^whyysmtam",
             'email': ''},
            follow=True
        )
        post_user_count = FinetoothUser.objects.count()
        self.assertEqual(prior_user_count, post_user_count)
        self.assertEqual(422, response.status_code)


class TaggingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.the_user = f.FinetoothUserFactory.create()
        cls.other_user = f.FinetoothUserFactory.create()
        cls.the_post = f.PostFactory.create(author=cls.the_user)
        cls.other_post = f.PostFactory.create()
        cls.extant_tag = f.TagFactory.create()
        cls.the_post.tag_set.add(cls.extant_tag)

    def setUp(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )

    def concerning_users_tagging_their_own_posts(self):
        self.client.post(reverse('tag', args=(self.the_post.pk,)),
                         {'label': "taggable"})
        tags = self.the_post.tag_set
        self.assertTrue("taggable", tags.filter(label="taggable").exists())

    def concerning_users_inability_to_tag_posts_of_others(self):
        response = self.client.post(
            reverse('tag', args=(self.other_post.pk,)),
            {'label': "untaggable"}
        )
        self.assertEqual(403, response.status_code)
        tags = self.other_post.tag_set
        self.assertEqual(0, tags.count())

    def concerning_prohibition_of_double_tagging(self):
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

class CommentingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.the_user = f.FinetoothUserFactory.create()
        cls.the_post = f.PostFactory.create()

    def concerning_comment_submission(self):
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

    def concerning_html_injection(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse("add_comment", args=(self.the_post.pk,)),
            {'content': "and it's what my <textarea>"}
        )
        comment = self.the_post.comment_set.filter(commenter=self.the_user)[0]
        self.assertNotIn("<textarea>", comment.content)

    def concerning_blank_comment_submissions(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse("add_comment", args=(self.the_post.pk,)),
            {'content': ""}
        )
        self.assertNotEqual(500, response.status_code)


class BallotBoxTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.the_user = f.FinetoothUserFactory.create()
        cls.the_post = f.PostFactory.create(content="hello Django world")

    def concerning_suffrage(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        for start_index, end_index in ((0, 1), (1, 3), (5, 8)):
            response = self.client.post(
                reverse('vote', args=("post", self.the_post.pk)),
                {'startIndex': start_index, 'endIndex': end_index,
                 'value': 1}
            )
            self.assertEqual(response.status_code, 204)


    def concerning_suffrage_of_undocumented_immigrants(self):
        response = self.client.post(
            reverse('vote', args=("post", self.the_post.pk)),
            {'startIndex': 1, 'endIndex': 5, 'value': 1}
        )
        self.assertEqual(response.status_code, 401)

    def concerning_hanging_chads(self):
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

    def concerning_the_principle_of_one_user_one_vote(self):
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        response = self.client.post(
            reverse('vote', args=("post", self.the_post.pk)),
            {'startIndex': 0, 'endIndex': 5, 'value': 1}
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.post(
            reverse('vote', args=("post", self.the_post.pk)),
            {'startIndex': 2, 'endIndex': 4, 'value': 1}
        )
        self.assertContains(response, "Overlapping votes are not allowed!",
                            status_code=403)

class ProfileTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        FinetoothUser.objects.create_user(
            username="Jennifer_Userton", password="vmR9*sdfp["
        )
        FinetoothUser.objects.create_user(
            username="Not_Jennifer", password="shsk$&hfio"
        )

    def concerning_nonexistent_users(self):
        response = self.client.get(
            reverse('show_profile', args=("nonexistent2507",)), follow=True)
        self.assertContains(response, "That user does not exist.")

    def concerning_profile_editing(self):
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

    def concerning_editing_the_profiles_of_others(self):
        self.client.login(username="Jennifer_Userton", password="vmR9*sdfp[")
        response = self.client.post(
            reverse('edit_profile', args=("Not_Jennifer",)),
            {'url': "http://example.com/ju",
             'location': "Usertown, California"}
        )
        self.assertEqual(403, response.status_code)


class PostTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        FinetoothUser.objects.create_user(
            username="Jennifer_Userton", password="vmR9*sdfp["
        )

    def setUp(self):
        self.client.login(username="Jennifer_Userton", password="vmR9*sdfp[")

    def concerning_new_posts(self):
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


class PaginationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 11):
            f.PostFactory.create(
                title="Pagination {}".format(romanize(i)),
                published_at=datetime.now()-timedelta(10-i)
            )

    def concerning_pagination(self):
        with self.settings(POSTS_PER_PAGE=3):
            pages = [self.client.get(reverse('home', args=(i,)))
                     for i in range(1, 5)]
        installment_groups = [
            ('X', 'IX', 'VIII'), ('VII', 'VI', 'V'),
            ('IV', 'III', 'II'), ('I',)
        ]
        for page_index, installment_group in enumerate(installment_groups):
            for part_no in installment_group:
                with self.subTest(page_no=page_index+1):
                    self.assertContains(
                        pages[page_index], "Pagination {}".format(part_no)
                    )
