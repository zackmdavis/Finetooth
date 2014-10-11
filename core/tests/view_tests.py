from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from core.models import FinetoothUser, Post
from core.tests import factories as f

class TaggingTest(TestCase):

    def setUp(self):
        self.the_user = f.FinetoothUserFactory.create()
        self.other_user = f.FinetoothUserFactory.create()
        self.the_post = f.PostFactory.create(author=self.the_user)
        self.other_post = f.PostFactory.create()
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )

    def test_user_can_tag_own_post(self):
        self.client.post(reverse('tag', args=(self.the_post.pk,)),
                         {'label': "user can tag own post"})
        tags = self.the_post.tag_set
        self.assertEqual(1, tags.count())
        self.assertEqual("user can tag own post", tags.first().label)

    def test_user_cannot_tag_post_of_other(self):
        response = self.client.post(
            reverse('tag', args=(self.other_post.pk,)),
            {'label': "user cannot tag other user's post"}
        )
        self.assertEqual(403, response.status_code)
        tags = self.other_post.tag_set
        self.assertEqual(0, tags.count())


class CommentingTest(TestCase):

    def setUp(self):
        self.the_user = f.FinetoothUserFactory.create()
        self.the_post = f.PostFactory.create()

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

    def test_can_vote_on_post(self):
        selections = [{'selection': "hello", 'value': 1},
                      {'selection': "Django", 'value': 1},
                      {'selection': "h", 'value': 1}]
        self.client.login(
            username=self.the_user.username, password=f.FACTORY_USER_PASSWORD
        )
        for selection in selections:
            self.client.post(reverse('vote', args=("post", self.the_post.pk)),
                             selection)
        self.assertEqual(3, self.the_post.score)
        self.assertEqual((('h', 2), ('e', 1)),
                         self.the_post.scored_plaintext()[:2])
        self.assertEqual(('D', 1), self.the_post.scored_plaintext()[6])
        self.assertEqual(('d', 0), self.the_post.scored_plaintext()[-1])


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
