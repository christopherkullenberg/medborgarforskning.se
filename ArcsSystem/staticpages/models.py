from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager

from wagtail.core.models import Page as page_wagtail
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


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
    welcome_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='welcomeImage'
        )
    welcome_title = models.CharField(max_length=100, default='Welcome')
    welcome_body = models.TextField()
    project_title = models.CharField(max_length=100, default='Projects')
    project_body = models.TextField()
    get_CitSciSE_title = models.CharField(max_length=100, default='Get involved with CitSciSE')
    get_CitSciSE_body = models.TextField()
    data_quality_box_title = models.CharField(max_length=100, default='Data Quality')
    data_quality_box_subtitle = models.CharField(max_length=100, default='Getting Started')
    data_quality_box_body = models.TextField()
    paper_box_title = models.CharField(max_length=100, default='Papers')
    paper_box_subtitle = models.CharField(max_length=100, default='Recent papers')
    paper_box_body = models.CharField(max_length=200)
    CitSciSE_box_title = models.CharField(max_length=100, default='CitSciSE Community')
    CitSciSE_box_subtitle = models.CharField(max_length=100, default='Recent Blog Posts')
    CitSciSE_box_body = models.CharField(max_length=200)

    content_panels = page_wagtail.content_panels + [
        FieldPanel('welcome_title'),
        FieldPanel('welcome_body'),
        FieldPanel('project_title'),
        FieldPanel('project_body'),
        FieldPanel('get_CitSciSE_title'),
        FieldPanel('get_CitSciSE_body'),
        FieldPanel('data_quality_box_title'),
        FieldPanel('data_quality_box_subtitle'),
        FieldPanel('data_quality_box_body'),
        FieldPanel('paper_box_title'),
        FieldPanel('paper_box_subtitle'),
        FieldPanel('paper_box_body'),
        FieldPanel('CitSciSE_box_title'),
        FieldPanel('CitSciSE_box_subtitle'),
        FieldPanel('CitSciSE_box_body'),
        ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
        ImageChooserPanel('welcome_image'),
    ]

    template = 'home.html'

    def get_absolute_url(self):
        return reverse('staticpages:homepage_view')
