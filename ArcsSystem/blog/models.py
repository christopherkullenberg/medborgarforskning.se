from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.db.models.signals import pre_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from django.urls import reverse

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.core.signals import page_published

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

import datetime
import re

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

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    ''' Blog page Database fields'''

    template = 'blog/blog_list.html'

    blogAuthor = models.CharField(max_length=255)
    authorEmail = models.EmailField()
    publishedDate = models.DateField('Post date')
    blogTags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    body = StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])


    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('publishedDate'),
        index.FilterField('blogTags'),
    ]

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('blogAuthor'),
        FieldPanel('authorEmail'),
        FieldPanel('publishedDate'),
        StreamFieldPanel('body'),
        FieldPanel('blogTags'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    def get_absolute_url(self):
        #return reverse('blog:archive_date_detail', args={'pk' : str(self.id)})

        language_code = translation.get_language()
        if language_code == 'sv':
            return reverse('blog:archive_date_detail',
                           kwargs={'year' : self.publishedDate.year,
                                   'month' : self.publishedDate.month,
                                   'day' : self.publishedDate.day,
                                   'slug' : self.slug_sv #change from pk id
                                   })

        else:
            return reverse('blog:archive_date_detail',
                           kwargs={'year' : self.publishedDate.year,
                                   'month' : self.publishedDate.month,
                                   'day' : self.publishedDate.day,
                                   'slug' : self.slug_en #change from pk id
                                   })


# @receiver(pre_save, sender=BlogPage)
def receiver(sender,instance, **kwargs):
    if instance.title_sv != None and instance.slug_sv == None:
        title_sv = spinalcase(instance.title_sv)
        instance.slug_sv = title_sv
        instance.save()


page_published.connect(receiver, sender=BlogPage)

def lowercase(string):
    """Convert string into lower case.
    Args:
        string: String to convert.
    Returns:
        string: Lowercase case string.
    """

    return str(string).lower()

def snakecase(string):
    """Convert string into snake case.
    Join punctuation with underscore
    Args:
        string: String to convert.
    Returns:
        string: Snake cased string.
    """

    string = re.sub(r"[\-\.\s]", '_', str(string))
    if not string:
        return string
    return lowercase(string[0]) + re.sub(r"[A-Z]", lambda matched: '_' + lowercase(matched.group(0)), string[1:])


def spinalcase(string):
    """Convert string into spinal case.
    Join punctuation with hyphen.
    Args:
        string: String to convert.
    Returns:
        string: Spinal cased string.
    """

    return re.sub(r"_", "-", snakecase(string))
