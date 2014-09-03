from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from core.models import FinetoothUser, Post

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
