from django.db import models

# TODO: users

class Post(models.Model):
    # TODO: "author" attribute will be ForeignKey to user model
    content = models.TextField()

class Comment(models.Model):
    # TODO: "author" attribute will be, &c.
    content = models.TextField()
    post = models.ForeignKey("Post")
    
