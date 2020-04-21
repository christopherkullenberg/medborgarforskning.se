from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse


class Post(models.Model):
    '''
    This is the basic model for a blog post
    '''
    title = models.CharField(max_length=100, default='title')
    published = models.DateField()
    content = models.TextField()
    tags = TaggableManager()

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse ('post_detail',
    #        args=[published.created_on.year, published.created_on.strftime('%m'),
    #        published.created_on.strftime('%d'), self.title])


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name
