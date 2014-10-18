import logging
from html.parser import HTMLParser

from markdown import markdown

logger = logging.getLogger(__name__)

class Tagnostic(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.content = []
        self.feed(markdown(content))

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

    def accept_vote(self, voter, selection, value):
        # XXX what about when the selection appears more than
        # once?--search by regex instead and disallow voting on
        # non-unique phrases? Or can we do better?
        start_index = self.plaintext.find(selection)
        if start_index != -1:
            end_index = start_index + len(selection)
            return self.vote_set.create(
                voter=voter, value=value,
                start_index=start_index, end_index=end_index
            )
        else:
            logger.info(
                "invalid vote selection on {} #{}: {}".format(
                    self.__class__.__name__, self.pk, selection
                )
            )
            raise VotingException("Can't find selection in content!")

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
                        " " if attributes else "",
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
