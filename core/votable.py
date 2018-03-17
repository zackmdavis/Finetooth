import itertools
import logging
from html.parser import HTMLParser

from markdown import markdown as markdown_to_html

from django.db.models import Q

from django.utils.functional import SimpleLazyObject
from typing import List, Optional, Tuple, Union, Any


logger = logging.getLogger(__name__)

class Tagnostic(HTMLParser):
    def __init__(self, content: str) -> None:
        super().__init__(convert_charrefs=False)
        self.content = []
        self.feed(markdown_to_html(content, lazy_ol=False))

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        self.content.append((tag, dict(attrs)))

    def handle_endtag(self, tag: str) -> None:
        self.content.append(('/'+tag,))

    def handle_data(self, data: str) -> None:
        self.content.append(data)

    def plaintext(self) -> str:
        return ''.join(
            token for token in self.content if isinstance(token, str)
        )


class VotingException(Exception):
    pass


class VotableMixin:

    @property
    def score(self) -> int:
        return sum(v.value for v in self.vote_set.all())

    @property
    def plaintext(self) -> str:
        return Tagnostic(self.content).plaintext()

    def scored_plaintext(self, for_voter=None):
        plaintext = Tagnostic(self.content).plaintext()
        score_increments = [0] * (len(plaintext) + 1)
        mark_increments = [0] * (len(plaintext) + 1)
        for vote in self.vote_set.all():
            score_increments[vote.start_index] += vote.value
            score_increments[vote.end_index] -= vote.value
            if for_voter and vote.voter == for_voter:
                mark_increments[vote.start_index] += vote.value
                mark_increments[vote.end_index] -= vote.value
        return tuple(zip(plaintext,
                         itertools.accumulate(score_increments),
                         itertools.accumulate(mark_increments)))

    @staticmethod
    def _render_scored_substring(scored_characters: List[Tuple[str, int, int]]) -> str:
        join_to_render_partial = []
        value_at_index = None
        mark_at_index = None
        open_span = False
        for character, value, mark in scored_characters:
            if value == value_at_index and mark == mark_at_index:
                join_to_render_partial.append(character)
            else:
                if open_span:
                    join_to_render_partial.append('</span>')
                    open_span = False
                join_to_render_partial.append(
                    '<span title="score: {0}" data-value="{0}" data-mark="{1}">'.format(value, mark)
                )
                open_span = True
                value_at_index = value
                mark_at_index = mark
                join_to_render_partial.append(character)
        if open_span:
            join_to_render_partial.append('</span>')
        return ''.join(join_to_render_partial)

    def render(self) -> str:
        for_voter = getattr(self, 'request_user', None)
        parsed_content = Tagnostic(self.content).content
        # XXX inefficiency
        scored_plaintext_stack = list(
            reversed(self.scored_plaintext(for_voter)))
        join_to_render = []
        for token in parsed_content:
            if isinstance(token, str):  # text
                scored_characters = [scored_plaintext_stack.pop()
                                     for _ in range(len(token))]
                join_to_render.append(
                    self._render_scored_substring(scored_characters)
                )
            elif isinstance(token, tuple) and len(token) == 2:  # open tag
                tag_type, attributes = token
                join_to_render.append(
                    "<{}{}{}>".format(
                        tag_type,
                        " " if attributes else "",
                        " ".join(
                            '{}="{}"'.format(k, v)
                            for k, v in attributes.items()
                        )
                    )
                )
            elif isinstance(token, tuple) and len(token) == 1:  # close tag
                join_to_render.append("<{}>".format(token[0]))
        return "".join(join_to_render)

    def low_score(self) -> int:
        return min(v for c, v, _m in self.scored_plaintext())

    def high_score(self) -> int:
        return max(v for c, v, _m in self.scored_plaintext())

    def vote_in_range_for_user(self, voter: SimpleLazyObject,
                               ballot_start_index: int, ballot_end_index: int) -> Optional[Any]:
        return self.vote_set.filter(
            end_index__gt=ballot_start_index, start_index__lt=ballot_end_index,
            voter=voter
        ).first()
