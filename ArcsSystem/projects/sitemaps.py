from django.contrib.sitemaps import Sitemap
from .models import Project

class ProjectSitemap(Sitemap):

    def items(self):
        return Project.objects.all()

    def location(self, item):
        # return item.get_absolute_url()
        return item.get_absolute_url_details()
