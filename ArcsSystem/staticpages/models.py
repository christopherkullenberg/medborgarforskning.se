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
    category = models.SlugField(default="uncategorized")
    title = models.CharField(max_length=100, default='title')
    published = models.DateField()
    content = models.TextField()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('staticpages:staticpage',
                       kwargs={'category' : self.category,
                               'slug' : self.slug
                               })

    def get_category_url(self):
        return reverse('staticpages:staticpage',
                       kwargs={'category' : self.category
                               })

    def __str__(self):
        return self.title
