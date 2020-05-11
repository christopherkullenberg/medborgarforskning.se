from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager



class Page(models.Model):
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

    def __str__(self):
        return self.title
