from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.urls import reverse

import datetime


class Post(models.Model):
    '''
    This is the basic model for a blog post.

    Summernote Warning: Please mind, that the widget does not provide any escaping.
    If you expose the widget to external users without taking care of this,
    it could potentially lead to an injection vulnerability.
    Therefore you can use the SummernoteTextFormField or SummernoteTextField,
    which escape all harmful tags through mozilla's package bleach:
    https://github.com/summernote/django-summernote
    '''
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    slug = models.SlugField()
    title = models.CharField(max_length=100, default=_('title'))
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
    '''Basic author placeholder in the blog'''
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name
