from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from core.models import FinetoothUser, Post, Comment, Tag

class LatestAbstractContentFeed(Feed):

    def items(self):
        return Post.objects.order_by('-published_at')[:20]

    def item_title(self, content):
        return content.title

    def item_description(self, content):
        return content.content[:500] + "[...]"

    def item_pubdate(self, content):
        return content.published_at


class LatestPostsFeed(LatestAbstractContentFeed):
    title = "Finetooth Latest Posts"
    link = "/feeds/rss/"
    description = "latest posts on Finetooth"


class AbstractUserContentFeed(LatestAbstractContentFeed):
    def get_object(self, request, username):
        return get_object_or_404(FinetoothUser, username=username)

    def title(self, user):
        return "Latest Finetooth {}s for {}".format(
            self.model.__name__.title(), user.username)

    def link(self, user):
        return "/user/{}/feeds/{}s/rss/".format(
            user.username, self.model.__name__.lower())

    def description(self, user):
        return "latest Finetooth {}s by {}".format(
            self.model.__name__.lower(), user.username)

    def items(self, user):
        return self.model.objects.filter(
            **{'{}__username'.format(
                self.model_creator_job_title): user.username}
        ).order_by('-published_at')[:20]


class AuthorFeed(AbstractUserContentFeed):
    model = Post
    model_creator_job_title = "author"

class CommenterFeed(AbstractUserContentFeed):
    model = Comment
    model_creator_job_title = "commenter"


class TagFeed(LatestAbstractContentFeed):
    def get_object(self, request, label):
        return get_object_or_404(Tag, label=label)

    def title(self, tag):
        return "Latest Finetooth Posts Tagged With '{}'".format(tag.label)

    def link(self, tag):
        return "/tagged/{}/feeds/rss/".format(tag.label)

    def description(self, tag):
        return "latest Finetooth posts tagged with '{}'".format(tag.label)

    def items(self, tag):
        return tag.posts.order_by('-published_at')[:20]
