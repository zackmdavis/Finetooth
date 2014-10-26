import logging
from html.parser import HTMLParser

from markdown import markdown as markdown_to_html

logger = logging.getLogger(__name__)

class Tagnostic(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.content = []
        self.feed(markdown_to_html(content, lazy_ol=False))

    def handle_starttag(self, tag, attrs):
        self.content.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        self.content.append(('/'+tag,))

    def handle_data(self, data):
        self.content.append(data)

    def plaintext(self):
        return ''.join(
            token for token in self.content if isinstance(token, str)
        )


class VotingException(Exception):
    pass


class VotableMixin:

    @property
    def score(self):
        return sum(v.value for v in self.vote_set.all())

    @property
    def plaintext(self):
        return Tagnostic(self.content).plaintext()

    def scored_plaintext(self):
        votes = self.vote_set.all()
        scored_characters = []
        # XXX inefficient
        for i, c in enumerate(Tagnostic(self.content).plaintext()):
            score = sum(
                v.value for v in votes if v.start_index <= i < v.end_index
            )
            scored_characters.append((c, score))
        return tuple(scored_characters)


    @staticmethod
    def _render_scored_substring(scored_characters):
        join_to_render_partial = []
        value_at_index = None
        open_span = False
        for character, value in scored_characters:
            if value == value_at_index:
                join_to_render_partial.append(character)
            else:
                if open_span:
                    join_to_render_partial.append('</span>')
                    open_span = False
                join_to_render_partial.append(
                    '<span data-value="{}">'.format(value)
                )
                open_span = True
                value_at_index = value
                join_to_render_partial.append(character)
        if open_span:
            join_to_render_partial.append('</span>')
        return ''.join(join_to_render_partial)

    def render(self):
        parsed_content = Tagnostic(self.content).content
        # XXX inefficiency
        scored_plaintext_stack = list(reversed(self.scored_plaintext()))
        join_to_render = []
        for token in parsed_content:
            if isinstance(token, str): # text
                scored_characters = [scored_plaintext_stack.pop()
                                     for _ in range(len(token))]
                join_to_render.append(
                    self._render_scored_substring(scored_characters)
                )
            elif isinstance(token, tuple) and len(token) == 2: # open tag
                tag_type, attributes = token
                join_to_render.append(
                    "<{}{}{}>".format(
                        tag_type,
                        " " if attributes else '',
                        " ".join(
                            '{}="{}"'.format(k, v)
                            for k, v in attributes.items()
                        )
                    )
                )
            elif isinstance(token, tuple) and len(token) == 1: # close tag
                join_to_render.append("<{}>".format(token[0]))
        return "".join(join_to_render)

    def low_score(self):
        return min(v for c, v in self.scored_plaintext())

    def high_score(self):
        return max(v for c, v in self.scored_plaintext())


class IndirectlyScorableMixin:

    @property
    def score(self):
        return sum(v.score for v in self.associated_votable_set.all())

    @classmethod
    def low_score(cls):
        if cls.objects.exists():
            return min(i.score for i in cls.objects.all())
        else:
            return 0

    @classmethod
    def high_score(cls):
        if cls.objects.exists():
            return max(i.score for i in cls.objects.all())
        else:
            return 0
