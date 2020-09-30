from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.search import index
from wagtail.core.signals import page_published
from wagtail.core.models import Page as page_wagtail
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import(
                                FieldPanel,
                                MultiFieldPanel,
                                InlinePanel,
                                StreamFieldPanel,
                                FieldRowPanel)
from .edit_handlers import ReadOnlyPanel

import datetime
import re

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

    max_count = 1

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
    max_count = 1


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
    max_count = 1


class SourcecodePage(page_wagtail):
    ''' basic page for source code '''
    template = 'staticpages/source_code.html'

    sourcecode_title = models.CharField(max_length=100, default='Source Code')
    sourcecode_content = RichTextField()
    repository = models.URLField()

    content_panels = page_wagtail.content_panels + [
        ReadOnlyPanel('sourcecode_title', heading='Title'),
        FieldPanel('sourcecode_content'),
        FieldPanel('repository')
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
        ]
    max_count = 1


class PressPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PressPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class PressPage(page_wagtail):
    ''' basic page for Press '''

    template = 'staticpages/press_list.html'

    press_title = models.CharField(max_length=100, default='title')
    contact_Email = models.EmailField()
    pressPublishedDate = models.DateField('Post date')
    pressTags = ClusterTaggableManager(through=PressPageTag, blank=True)

    press_body = StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])


    # Search index configuration

    search_fields = page_wagtail.search_fields + [
        index.SearchField('press_body'),
        index.FilterField('pressPublishedDate'),
        index.FilterField('pressTags'),
    ]

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        FieldPanel('press_title'),
        FieldPanel('contact_Email'),
        FieldPanel('pressPublishedDate'),
        StreamFieldPanel('press_body'),
        FieldPanel('pressTags'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    def get_absolute_url(self):
        language_code = translation.get_language()
        if language_code == 'sv':
            return reverse('staticpages:archive_date_detail',
                           kwargs={'year' : self.pressPublishedDate.year,
                                   'month' : self.pressPublishedDate.month,
                                   'day' : self.pressPublishedDate.day,
                                   'slug' : self.slug_sv #change from pk id
                                   })

        else:
            return reverse('staticpages:archive_date_detail',
                           kwargs={'year' : self.pressPublishedDate.year,
                                   'month' : self.pressPublishedDate.month,
                                   'day' : self.pressPublishedDate.day,
                                   'slug' : self.slug_en #change from pk id
                                   })

class CitizenSciencePage(page_wagtail):
    template_name = 'staticpages/getting_started.html'

    citizen_science_menu_title = models.CharField(max_length=100, default='Getting started with Citizen Science')
    content_panels = page_wagtail.content_panels + [
        FieldPanel('citizen_science_menu_title'),
        ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    # Parent page / subpage type rules
    subpage_types = ['staticpages.CaseStudiesPage',
                     'staticpages.FAQPage',
                     'staticpages.AdditionalResourcesPage',
                     'staticpages.WhatsCitizenSciencePage']
    parent_page_types = ['wagtailcore.Page']

    # max_count = 1

    def get_absolute_url(self):
        return reverse('staticpages:getting_started',
                       kwargs={
                               'slug' : self.title #change from pk id
                               })


# class WhatIsCitizenSciencePage(page_wagtail):
#     template_name = 'staticpages/what_is_citizen_science.html'
#
#     what_citizen_science_body =  StreamField([
#         ('title', blocks.CharBlock(classname='full title')),
#         ('content', blocks.RichTextBlock()),
#     ])
#     # Editor panels configuration
#     content_panels = page_wagtail.content_panels + [
#         StreamFieldPanel('what_citizen_science_body'),
#     ]
#
#     promote_panels = [
#         MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
#     ]
#
#     # subpage_types = ['staticpages.SwedishCitizenSciencePage']
#     # parent_page_types = ['staticpages.CitizenSciencePage']
#
#     max_count = 1
#
#     def get_url_parts(self, *args, **kwargs):
#         url_parts = super(WhatIsCitizenSciencePage, self).get_url_parts(*args, **kwargs)
#
#         if url_parts is None:
#             # in this case, the page doesn't have a well-defined URL in the first place -
#             # for example, it's been created at the top level of the page tree
#             # and hasn't been associated with a site record
#             return None
#
#         site_id, root_url, page_path = url_parts
#         page_path = page_path.replace("pages/","")
#
#         # return '/' in place of the real page path
#         return (site_id, root_url, page_path)

class WhatsCitizenSciencePage(page_wagtail):

    template_name = 'staticpages/what_is_citizen_science.html'

    citizen_science_body =  StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('citizen_science_body'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    subpage_types = ['staticpages.SwedishCitizenSciencePage']
    max_count = 1

    def get_url_parts(self, *args, **kwargs):
        url_parts = super(WhatsCitizenSciencePage, self).get_url_parts(*args, **kwargs)

        if url_parts is None:
            # in this case, the page doesn't have a well-defined URL in the first place -
            # for example, it's been created at the top level of the page tree
            # and hasn't been associated with a site record
            return None

        site_id, root_url, page_path = url_parts
        page_path = page_path.replace("pages/","")

        # return '/' in place of the real page path
        return (site_id, root_url, page_path)


class SwedishCitizenSciencePage(page_wagtail):

    template_name = 'staticpages/swedish_citizen_science.html'

    swedish_citizen_science_body =  StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('swedish_citizen_science_body'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    subpage_types = []
    parent_page_types = ['staticpages.WhatsCitizenSciencePage']
    max_count = 1

    def get_url_parts(self, *args, **kwargs):
        url_parts = super(SwedishCitizenSciencePage, self).get_url_parts(*args, **kwargs)

        if url_parts is None:
            # in this case, the page doesn't have a well-defined URL in the first place -
            # for example, it's been created at the top level of the page tree
            # and hasn't been associated with a site record
            return None

        site_id, root_url, page_path = url_parts
        page_path = page_path.replace("pages/","")

        # return '/' in place of the real page path
        return (site_id, root_url, page_path)


class CaseStudiesPage(page_wagtail):

    template_name = 'staticpages/case_studies.html'

    case_studies_body =  StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('case_studies_body'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    subpage_types = []
    parent_page_types = ['staticpages.CitizenSciencePage']
    max_count = 1

    def get_url_parts(self, *args, **kwargs):
        url_parts = super(CaseStudiesPage, self).get_url_parts(*args, **kwargs)

        if url_parts is None:
            # in this case, the page doesn't have a well-defined URL in the first place -
            # for example, it's been created at the top level of the page tree
            # and hasn't been associated with a site record
            return None

        site_id, root_url, page_path = url_parts
        page_path = page_path.replace("pages/","")

        # return '/' in place of the real page path
        return (site_id, root_url, page_path)


class FAQPage(page_wagtail):

    template_name = 'staticpages/faq.html'

    faq_body =  StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('faq_body'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    subpage_types = []
    parent_page_types = ['staticpages.CitizenSciencePage']
    max_count = 1

    def get_url_parts(self, *args, **kwargs):
        url_parts = super(FAQPage, self).get_url_parts(*args, **kwargs)

        if url_parts is None:
            # in this case, the page doesn't have a well-defined URL in the first place -
            # for example, it's been created at the top level of the page tree
            # and hasn't been associated with a site record
            return None

        site_id, root_url, page_path = url_parts
        page_path = page_path.replace("pages/","")

        # return '/' in place of the real page path
        return (site_id, root_url, page_path)


class AdditionalResourcesPage(page_wagtail):

    template_name = 'staticpages/additional_resources.html'

    additional_resources_body =  StreamField([
        ('title', blocks.CharBlock(classname='full title')),
        ('content', blocks.RichTextBlock()),
    ])

    # Editor panels configuration
    content_panels = page_wagtail.content_panels + [
        StreamFieldPanel('additional_resources_body'),
    ]

    promote_panels = [
        MultiFieldPanel(page_wagtail.promote_panels, "Common page configuration"),
    ]

    subpage_types = []
    parent_page_types = ['staticpages.CitizenSciencePage']
    max_count = 1

    def get_url_parts(self, *args, **kwargs):
        url_parts = super(AdditionalResourcesPage, self).get_url_parts(*args, **kwargs)

        if url_parts is None:
            # in this case, the page doesn't have a well-defined URL in the first place -
            # for example, it's been created at the top level of the page tree
            # and hasn't been associated with a site record
            return None

        site_id, root_url, page_path = url_parts
        page_path = page_path.replace("pages/","")

        # return '/' in place of the real page path
        return (site_id, root_url, page_path)


def receiver(sender,instance, **kwargs):
    if instance.title_sv != None and instance.slug_sv == None:
        title_sv = spinalcase(instance.title_sv)
        instance.slug_sv = title_sv
        instance.save()


page_published.connect(receiver, sender=PressPage)

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
