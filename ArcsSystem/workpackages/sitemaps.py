from django.contrib.sitemaps import Sitemap
from .models import WorkPackage

class WorkPackageSitemap(Sitemap):

    def items(self):
        return WorkPackage.objects.all()

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, obj):
        return obj.published
