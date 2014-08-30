from django.test import TestCase

from core.models import Post

class ScoringTest(TestCase):

    def setUp(self):
        self.the_post = Post.objects.create(content="friendship")
        for i in range(6):
            self.the_post.vote_set.create(value=1, start_index=i, end_index=10)

    def test_scored_content(self):
        self.assertEqual(
            self.the_post.scored_content,
            (('f', 1), ('r', 2), ('i', 3), ('e', 4), ('n', 5), ('d', 6),
             ('s', 6), ('h', 6), ('i', 6), ('p', 6))
        )
