class VotableMixin:

    @property
    def score(self):
        return sum(v.value for v in self.vote_set.all())

    @property
    def scored_content(self):
        votes = self.vote_set.all()
        scored_characters = []
        # XXX FIXME: O(n^2) in the length of content; I think we can
        # and may need to do better than that
        for i, c in enumerate(self.content):
            score = sum(
                v.value for v in votes if v.start_index <= i < v.end_index
            )
            scored_characters.append((c, score))
        return tuple(scored_characters)

    def render(self):
        return "".join(
            "<span data-value=\"{}\">{}</span>".format(value, character)
            for character, value in self.scored_content
        )

    def low_score(self):
        return min(v for c, v in self.scored_content)

    def high_score(self):
        return max(v for c, v in self.scored_content)
