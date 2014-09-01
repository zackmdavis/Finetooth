from django.test import TestCase

from markdown import markdown

from core.models import Post
from core.votable import Tagnostic

class TagnosticismTest(TestCase):

    def test_feeding(self):
        content = markdown("*Hello* [Python](python.org) world")
        tag_skeptic = Tagnostic(content)
        self.assertEqual(
            tag_skeptic.content,
            [('p', {}), ("em", {}), "Hello", ("/em",), " ",
             ('a', {'href': 'python.org'}), "Python", ("/a",),
             " world", ('/p',)]
        )

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

    def test_scored_content(self):
        self.assertEqual(
            self.the_post.scored_content,
            (('f', 1), ('r', 2), ('i', 3), ('e', 4), ('n', 5), ('d', 6),
             ('s', 6), ('h', 6), ('i', 6), ('p', 6))
        )
