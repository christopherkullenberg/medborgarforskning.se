from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse


class Post(models.Model):
    '''
    This is the basic model for a blog post
    '''
    title = models.CharField(max_length=100, default='title')
    published = models.DateField()# todo make name more focused on date like datapublished - could be confused with published status
    content = models.TextField() #summernote field
    tags = TaggableManager()

    def __str__(self):
        return self.title

    # Ref doc - https://docs.djangoproject.com/en/2.2/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        return reverse('blog:blog_detail_view', args=[str(self.id)])


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name
