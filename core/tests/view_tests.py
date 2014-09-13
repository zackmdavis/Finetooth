from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from core.models import FinetoothUser, Post

class TaggingTest(TestCase):

    def setUp(self):
         self.the_user = FinetoothUser.objects.create_user(
             username="Jennifer_Userton", password="vmR7*sefp["
         )
         self.other_user = FinetoothUser.objects.create_user(
             username="Not_Jennifer", password="N3gnt0p3"
         )
         self.the_post = Post.objects.create(
             author=self.the_user, title="Tag Driven Development",
             content="Lorum ipsum taggable", published_at=datetime.now()
         )
         self.other_post = Post.objects.create(
             author=self.other_user, title="Better Than Ever",
             content="You can feel it; we are back",
             published_at=datetime.now()
         )
         self.client.login(username="Jennifer_Userton", password="vmR7*sefp[")

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


class BallotBoxTest(TestCase):

    def setUp(self):
        self.the_user = FinetoothUser.objects.create_user(
            username="test", password="password"
        )
        self.the_post = Post.objects.create(
            author_id=2,content="hello Django world",
            published_at=datetime.now()
        )

    def test_can_vote_on_post(self):
        selections = [{'selection': "hello", 'value': 1},
                      {'selection': "Django", 'value': 1},
                      {'selection': "h", 'value': 1}]
        for selection in selections:
            self.client.login(username="test", password="password")
            self.client.post(reverse('vote', args=("post", self.the_post.pk)),
                             selection)
        self.assertEqual(3, self.the_post.score)
        self.assertEqual((('h', 2), ('e', 1)),
                         self.the_post.scored_plaintext()[:2])
        self.assertEqual(('D', 1), self.the_post.scored_plaintext()[6])
        self.assertEqual(('d', 0), self.the_post.scored_plaintext()[-1])
