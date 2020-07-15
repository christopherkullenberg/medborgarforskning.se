from django.contrib.sitemaps import Sitemap
from .models import Post, Author

class BlogSitemap(Sitemap):

    def items(self):
        return Post.objects.all()

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, obj):
        return obj.published
