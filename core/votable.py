class VotableMixin:

    @property
    def score(self):
        return sum(v.value for v in self.vote_set.all())
