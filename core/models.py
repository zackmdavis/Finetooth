from django.db import models
from core.votable import VotableMixin

# TODO: users; probably want to subclass Django's AbstractUser

class Post(models.Model, VotableMixin):
    # TODO: "author" attribute will be ForeignKey to user model
    # TODO: "title" attribute should be CharField (but what should
    # max_length be??)
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
    # TODO: for the exciting unique feature of this project, we're
    # actually going to want votes to have a start and end index, so
    # that they refer to substrings within the content of a post
    # (respectively comment), rather than the post (respectively
    # comment) itself
    value = models.IntegerField()

class PostVote(Vote):
    post = models.ForeignKey("Post")

    def __str__(self):
        return "{} on post #{}".format(self.value, self.post.pk)

class CommentVote(Vote):
    comment = models.ForeignKey("Comment")

    def __str__(self):
        return "{} on comment #{}".format(self.value, self.comment.pk)
