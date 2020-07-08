from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os

STATUS_CHOICES = [
    ('0', 'Not Selected'),
    ('1', 'Not yet started'),
    ('2', 'Active'),
    ('3', 'Periodically active'),
    ('4', 'On hold'),
    ('5', 'Abandonded')
]

VISIBILTIY_CHOICES = [
    ('H', 'Hidden'),
    ('V', 'Visible')
]

UN_REGIONS_CHOICES = [
    ('NU', 'Not Selected'),
    ('AF', 'Africa'),
    ('SA', 'Americas-South America'),
    ('CA', 'Americas-Central America'),
    ('NA', 'Americas-North America'),
    ('AS', 'Asia'),
    ('EU', 'Europe'),
    ('OC', 'Oceana')
]

class Keyword(models.Model):
    '''Keywords for the projects'''
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

    keyword = models.TextField()
    def __str__(self):
        return f'{self.keyword}'

class Project(models.Model):
    ''' This defines the project model for which
    '''
    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    '''Required alphabetical'''
    aim = models.CharField(help_text=_('Primary focus of the project.'),max_length=200, default='')
    description = models.CharField(max_length=5000, default='')
    name = models.CharField(help_text=_('Common name for the project.'),max_length=200, default='')
    start_date = models.DateTimeField(help_text=_('Date the project started.'), null=True)
    end_date = models.DateTimeField(help_text=_('Date the project concluded.'), null=True)
    status = models.CharField(max_length=30, default='0', choices=STATUS_CHOICES)
    image_dir = models.CharField(max_length= 200, default= '')
    target_audience = models.CharField(help_text=_('Project primary audience.'),max_length=5000, default='')
    contact_name = models.CharField(help_text=_('Name of the person maintaining this entry. Default is your account.'),max_length=200, default='')
    contact_role = models.CharField(help_text=_('Maintainer’s role or position with this project.'),max_length=200, default='')
    contact_affiliation = models.CharField(help_text=_('Maintainer’s institutional affiliation.'),max_length=200, default='')
    contact_email = models.CharField(max_length=200, default='')
    contact_phone = models.CharField(max_length=200, default='')
    keywords = models.ManyToManyField(Keyword)

    # keywords
    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('projects:project_list')

    def get_absolute_url_details(self):
        return reverse('projects:project_detail', args=[str(self.id)])


    def __str__(self):
        return self.name


@receiver(post_save, sender=Project)
def generate_image_dir(sender, instance, created, **kwargs):
    if created:
        path = settings.MEDIA_ROOT + '/images/projects/' + str(instance.id)
        os.makedirs(path)
        instance.image_dir = '/media/images/projects/' + str(instance.id)
        instance.save()
