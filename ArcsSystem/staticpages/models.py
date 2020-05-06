from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Page(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100, default='title')
    published = models.DateField()
    content = models.TextField()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('staticpages:staticpage',
                       kwargs={'slug' : self.slug #change from pk id
                               })

    def __str__(self):
        return self.title
