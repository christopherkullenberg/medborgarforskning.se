from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager


class Page(models.Model):
    '''Defines a basic page'''
    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

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
