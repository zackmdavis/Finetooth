from datetime import datetime

from django.test import TestCase

from core.models import Post
from core.votable import Tagnostic

from core.tests.factories import (
    FinetoothUserFactory, PostFactory, PostVoteFactory)

class TagnosticismTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        content = "*Hello* [Python](python.org) world"
        self.tag_skeptic = Tagnostic(content)

    def concerning_feeding(self):
        self.assertEqual(
            self.tag_skeptic.content,
            [('p', {}), ("em", {}), "Hello", ("/em",), " ",
             ('a', {'href': 'python.org'}), "Python", ("/a",),
             " world", ('/p',)]
        )

    def concerning_plaintext(self):
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

    def concerning_scored_plaintext(self):
        self.assertEqual(
            self.the_post.scored_plaintext(),
            (('f', 1, 0), ('r', 2, 0), ('i', 3, 0), ('e', 4, 0), ('n', 5, 0),
             ('d', 6, 0), ('s', 6, 0), ('h', 6, 0), ('i', 6, 0), ('p', 6, 0))
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

    def concerning_rendering(self):
        self.assertHTMLEqual(
            self.the_post.render(),
            """<p>
                 <span title="score: 1" data-value="1" data-mark="0">We\'ll </span>
                 <em>
                   <span title="score: 1" data-value="1" data-mark="0">al</span>
                   <span title="score: 2" data-value="2" data-mark="0">ways</span>
                   <span title="score: 1" data-value="1" data-mark="0">find</span>
                   <span title="score: 0" data-value="0" data-mark="0"> a way</span>
                 </em>
                 <span title="score: 0" data-value="0" data-mark="0">
                    ; that\'s why the people of
                 </span>
                 <em>
                   <span title="score: 0" data-value="0" data-mark="0">this</span>
                 </em>
                 <span title="score: 0" data-value="0" data-mark="0">world believe</span>
               </p>"""
        )
