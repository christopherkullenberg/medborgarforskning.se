from django.contrib.sitemaps import Sitemap
from .models import Article

class PublicationSitemap(Sitemap):

    def items(self):
        return Article.objects.all()

    def location(self, item):
        return item.get_absolute_url()
