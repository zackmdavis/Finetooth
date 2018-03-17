from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

from core.votable import VotableMixin


class FinetoothUser(AbstractUser):
    location = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)

    def post_karma(self) -> int:
        return 3 * sum(post.score for post in self.post_set.all())

    def comment_karma(self) -> int:
        return sum(comment.score for comment in self.comment_set.all())

    def karma(self) -> int:
        return self.post_karma() + self.comment_karma()


class Post(models.Model, VotableMixin):
    author = models.ForeignKey("FinetoothUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(
        validators=[
            MinLengthValidator(
                5, "Posts must contain at least five characters."),
        ]
    )
    published_at = models.DateTimeField()
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('show_post', args=(self.year, self.month, self.slug))

    def __str__(self):
        return "#{}: {}".format(self.pk, self.title)

    @property
    def month(self) -> str:
        return str(self.published_at.month).zfill(2)

    @property
    def year(self) -> str:
        return str(self.published_at.year).zfill(4)

    @property
    def vote_set(self):
        return self.postvote_set

    class Meta:
        ordering = ('-published_at',)


class Comment(models.Model, VotableMixin):
    commenter = models.ForeignKey("FinetoothUser", on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    parent = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{}; on \"{}\"".format(self.pk, self.post.title)

    def get_absolute_url(self):
        return (
            reverse('show_post',
                    args=(self.post.year, self.post.month, self.post.slug)) +
            "#comment-{}".format(self.pk)
        )

    @property
    def title(self):
        return "comment by {} on {} at {:%d %B %Y %H:%M}".format(
            self.commenter.username, self.post.title, self.published_at
        )

    @property
    def vote_set(self):
        return self.commentvote_set

    class Meta:
        ordering = ('published_at',)


class Vote(models.Model):
    voter = models.ForeignKey("FinetoothUser", on_delete=models.CASCADE)
    value = models.IntegerField()
    start_index = models.PositiveIntegerField()
    end_index = models.PositiveIntegerField()

class PostVote(Vote):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return "{} on post #{}".format(self.value, self.post.pk)

class CommentVote(Vote):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)

    def __str__(self):
        return "{} on comment #{}".format(self.value, self.comment.pk)


class Tag(models.Model):
    label = models.CharField(max_length=64, unique=True)
    posts = models.ManyToManyField("Post")

    def __str__(self) -> str:
        return self.label
