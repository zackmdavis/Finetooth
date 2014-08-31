from django.db import models
from django.contrib.auth.models import AbstractUser
from core.votable import VotableMixin

class FinetoothUser(AbstractUser):
    location = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)

class Post(models.Model, VotableMixin):
    author = models.ForeignKey("FinetoothUser")
    title = models.CharField(max_length=200)
    content = models.TextField()
    # TODO: date published (a DateTimeField)

    def __str__(self):
        return "#{}: {}".format(self.pk, self.title)

    @property
    def vote_set(self):
        return self.postvote_set


class Comment(models.Model, VotableMixin):
    commenter = models.ForeignKey("FinetoothUser")
    content = models.TextField()
    post = models.ForeignKey("Post")
    parent = models.ForeignKey("Comment", null=True)

    def __str__(self):
        return "#{} on \"{}\"".format(self.pk, self.post.title)

    @property
    def vote_set(self):
        return self.commentvote_set

class Vote(models.Model):
    voter = models.ForeignKey("FinetoothUser")
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
