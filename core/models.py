from django.db import models
from django.contrib.auth.models import AbstractUser
from core.votable import VotableMixin

class FinetoothUser(AbstractUser):   
    location = models.CharField(max_length=100)
    url = models.URLField()

class Post(models.Model, VotableMixin):
    author = models.ForeignKey("FinetoothUser")
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
    commenter = models.ForeignKey("FinetoothUser")
    content = models.TextField()
    post = models.ForeignKey("Post")
    
    def __str__(self):
        # TODO: change this to something more informative, &c.
        return "#{}: {}".format(self.pk, self.content[:12])

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


