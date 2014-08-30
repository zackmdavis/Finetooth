from django.test import TestCase
from django.core.urlresolvers import reverse

from core.models import Post

class BallotBoxTest(TestCase):

    def setUp(self):
        self.the_post = Post.objects.create(content="hello Django world")

    def test_can_vote_on_post(self):
        self.client.post(reverse('vote', args=("post", "1", "1")))
        self.client.post(reverse('vote', args=("post", "1", "2")))
        self.client.post(reverse('vote', args=("post", "1", "3")))
        lst_rspnse = self.client.post(reverse('vote', args=("post", "1", "1")))
        self.assertEqual(204, lst_rspnse.status_code)
        self.assertEqual(7, self.the_post.score)
