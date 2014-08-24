from django.db import models

# TODO: users

class Post(models.Model):
    # TODO: "author" attribute will be ForeignKey to user model
    # TODO: "title" attribute should be CharField (but what should
    # max_length be??)
    content = models.TextField()

    def __str__(self):
        # TODO: change this to something more informative when we have
        # authors and titles
        return "#{}: {}".format(self.pk, self.content[:12])
    

class Comment(models.Model):
    # TODO: "author" attribute will be, &c.
    content = models.TextField()
    post = models.ForeignKey("Post")
    
    def __str__(self):
        # TODO: change this to something more informative, &c.
        return "#{}: {}".format(self.pk, self.content[:12])
