from datetime import datetime

from django.test import TestCase

from core.models import Post
from core.votable import Tagnostic

from core.tests.factories import PostFactory, PostVoteFactory

class TagnosticismTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
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

class ScoringTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.the_post = Post.objects.create(
            author_id=1, content="friendship", title="eponymous",
            published_at=datetime.now()
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

class RenderingTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.the_post = PostFactory.create(
            content=("We'll *always find a way*; that's why the "
                     "people of *this* world believe")
        )
        upvote_indices = ((0, 12), (8, 17))
        for indices in upvote_indices:
            PostVoteFactory.create(
                post=self.the_post,
                start_index=indices[0], end_index=indices[1]
            )

    def test_rendering(self):
        self.assertHTMLEqual(
            self.the_post.render(),
            """<p>
                 <span data-value="1">We\'ll </span>
                 <em>
                   <span data-value="1">al</span>
                   <span data-value="2">ways</span>
                   <span data-value="1">find</span>
                   <span data-value="0"> a way</span>
                 </em>
                 <span data-value="0">; that\'s why the people of </span>
                 <em>
                   <span data-value="0">this</span>
                 </em>
                 <span data-value="0">world believe</span>
               </p>"""
        )
