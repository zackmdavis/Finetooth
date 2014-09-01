from django.test import TestCase

from core.models import Post
from core.votable import Tagnostic

class TagnosticismTest(TestCase):

    def setUp(self):
        content = "*Hello* [Python](python.org) world"
        self.tag_skeptic = Tagnostic(content)

    def test_feeding(self):
        self.assertEqual(
            self.tag_skeptic.content,
            [('p', {}), ("em", {}), "Hello", ("/em",), " ",
             ('a', {'href': 'python.org'}), "Python", ("/a",),
             " world", ('/p',)]
        )

    def test_plaintext(self):
        self.assertEqual(self.tag_skeptic.plaintext(), "Hello Python world")

class ScoringTest(TestCase):

    def setUp(self):
        self.the_post = Post.objects.create(
            author_id=1, content="friendship", title="eponymous"
        )
        for i in range(6):
            self.the_post.vote_set.create(
                voter_id=1, value=1,
                start_index=i, end_index=10
            )

    def test_scored_plaintext(self):
        self.assertEqual(
            self.the_post.scored_plaintext(),
            (('f', 1), ('r', 2), ('i', 3), ('e', 4), ('n', 5), ('d', 6),
             ('s', 6), ('h', 6), ('i', 6), ('p', 6))
        )
