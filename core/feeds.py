from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from core.models import FinetoothUser, Post

class LatestPostsFeed(Feed):
    title = "Finetooth Latest Posts"
    link = "/feeds/rss/"
    description = "latest posts on Finetooth"

    def items(self):
        return Post.objects.order_by('-published_at')[:20]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.content[:500] + "[...]"

    def item_pubdate(self, post):
        return post.published_at


class AuthorFeed(LatestPostsFeed):

    def get_object(self, request, username):
        return get_object_or_404(FinetoothUser, username=username)

    def title(self, author):
        return "Latest Finetooth Posts for {}".format(author.username)

    def link(self, author):
        return "/user/{}/feeds/posts/rss/".format(author.username)

    def description(self, author):
        return "latest Finetooth posts by {}".format(author.username)

    def items(self, author):
        return Post.objects.filter(
            author__username=author.username).order_by('-published_at')[:20]
