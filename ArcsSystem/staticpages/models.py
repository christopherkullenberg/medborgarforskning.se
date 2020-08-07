from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager

from wagtail.core.models import Page as page_wagtail
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel

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

class HomePage(page_wagtail):
    template = 'home.html'

    welcome_body = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='Welcome')),
        ('content', blocks.RichTextBlock()),
    ])

    project_body = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='Projects')),
        ('content', blocks.RichTextBlock()),
    ])

    get_CitSciSE_box = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='Get involved with CitSciSE')),
        ('content', blocks.RichTextBlock()),
    ])

    data_box = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='Data Quality')),
        ('subtitle', blocks.CharBlock(classname="full title", default='Getting Started')),
        ('content', blocks.RichTextBlock()),

    ])

    paper_box = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='Papers')),
        ('subtitle', blocks.CharBlock(classname="full title", default='Recent papers')),
    ])

    CitSciSE_box = StreamField([
        ('title', blocks.CharBlock(classname="full title", default='CitSciSE Community')),
        ('subtitle', blocks.CharBlock(classname="full title", default='Recent Blog Posts')),
        ])

    welcome_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='welcomeImage'
        )


    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('welcome_body'),
        StreamFieldPanel('project_body'),
        StreamFieldPanel('get_CitSciSE_box'),
        StreamFieldPanel('data_box'),
        StreamFieldPanel('paper_box'),
        StreamFieldPanel('CitSciSE_box'),
        ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
        ImageChooserPanel('welcome_image'),
    ]

    def get_absolute_url(self):
        return reverse('staticpages:homepage_view')


class TermsPage(page_wagtail):
    ''' basic page for terms '''

    template = 'staticpages/terms-cookies-privacy_detail.html'

    terms_title = models.CharField(max_length=100, default='title')
    version_number = models.CharField(max_length=100, default='v01')
    terms_content = RichTextField()

    content_panels = page_wagtail.content_panels + [
        FieldPanel('terms_title'),
        FieldPanel('version_number'),
        FieldPanel('terms_content')
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
        ]

class PrivacyPage(page_wagtail):
    ''' basic page for privacy '''

    template = 'staticpages/privacy.html'

    privacy_title = models.CharField(max_length=100, default='title')
    # version_number = models.CharField(max_length=100, default='v01')
    privacy_content = RichTextField()

    content_panels = page_wagtail.content_panels + [
        FieldPanel('privacy_title'),
        FieldPanel('privacy_content')
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
        ]
