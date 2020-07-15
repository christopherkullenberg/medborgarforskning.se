from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Organization

class OrganizationSitemap(Sitemap):

    def items(self):
        return Organization.objects.all()

    def location(self, item):
        return item.get_absolute_url()
