from django.db import models
from core.votable import VotableMixin

# TODO: users; probably want to subclass Django's AbstractUser

class Post(models.Model, VotableMixin):
    # TODO: "author" attribute will be ForeignKey to user model
    title = models.CharField(max_length=200)
    content = models.TextField()
    # TODO: date published (a DateTimeField), definitely! Maybe date
    # last edited (DateTimeField with auto_now), too?

    def __str__(self):
        # TODO: change this to something more informative when we have
        # authors and titles
        return "#{}: {}".format(self.pk, self.content[:12])

    @property
    def vote_set(self):
        return self.postvote_set


class Comment(models.Model, VotableMixin):
    # TODO: "author" attribute will be, &c.
    content = models.TextField()
    post = models.ForeignKey("Post")
    
    def __str__(self):
        # TODO: change this to something more informative, &c.
        return "#{}: {}".format(self.pk, self.content[:12])

    @property
    def vote_set(self):
        return self.commentvote_set


class Vote(models.Model):
    # TODO: "voter" attribute will be ForeignKey to User
    value = models.IntegerField()
    start_index = models.PositiveIntegerField()
    end_index = models.PositiveIntegerField()

class PostVote(Vote):
    post = models.ForeignKey("Post")

    def __str__(self):
        return "{} on post #{}".format(self.value, self.post.pk)

class CommentVote(Vote):
    comment = models.ForeignKey("Comment")

    def __str__(self):
        return "{} on comment #{}".format(self.value, self.comment.pk)
