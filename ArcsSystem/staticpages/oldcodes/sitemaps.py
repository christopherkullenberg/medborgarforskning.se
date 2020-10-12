from django.contrib.sitemaps import Sitemap
from .models import Page

class StaticpagesSitemap(Sitemap):

    def items(self):
        return Page.objects.all()

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, obj):
        return obj.published
