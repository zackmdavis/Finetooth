from django.contrib.syndication.views import Feed

from core.models import Post

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
