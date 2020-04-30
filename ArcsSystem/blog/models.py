from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse

import datetime


class Post(models.Model):
    '''
    This is the basic model for a blog post
    '''
    slug = models.SlugField()
    title = models.CharField(max_length=100, default='title')
    published = models.DateField()# todo make name more focused on date like datapublished - could be confused with published status
    content = models.TextField() #summernote field
    tags = TaggableManager()

    def __str__(self):
        return self.title

    # Ref doc - https://docs.djangoproject.com/en/2.2/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        #return reverse('blog:archive_date_detail', args={'pk' : str(self.id)})
        return reverse('blog:archive_date_detail',
                       kwargs={'year' : self.published.year,
                               'month' : self.published.month,
                               'day' : self.published.day,
                               'slug' : self.slug #change from pk id
                               })
        # instance.published|date:'Y', instance.published|date:'m', instance.published|date:'d' instance.id

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name
