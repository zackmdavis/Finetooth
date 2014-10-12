from django.db import models
from django.contrib.auth.models import AbstractUser
from core.votable import VotableMixin


class FinetoothUser(AbstractUser):
    location = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)

    def post_karma(self):
        return 3 * sum(post.score for post in self.post_set.all())

    def comment_karma(self):
        return sum(comment.score for comment in self.comment_set.all())

    def karma(self):
        return self.post_karma() + self.comment_karma()


class Post(models.Model, VotableMixin):
    author = models.ForeignKey("FinetoothUser")
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField()
    slug = models.SlugField(unique=True)

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
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{}; on \"{}\"".format(self.pk, self.post.title)

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


class Tag(models.Model):
    label = models.CharField(max_length=64, unique=True)
    posts = models.ManyToManyField("Post")

    def __str__(self):
        return self.label
