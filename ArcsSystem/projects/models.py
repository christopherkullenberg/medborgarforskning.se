from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os

# Define the options for the state of operation a project might be classified
# Defined here as used in more than one model
NOT_SELECTED = '0'
NOT_YET_STARTED = '1'
ACTIVE = '2'
PERIODICALLY_ACTIVE = '3'
ON_HOLD = '4'
ABANDONED = '5'
STATUS_CHOICES = [
    (NOT_SELECTED, 'Not Selected'),
    (NOT_YET_STARTED, 'Not yet started'),
    (ACTIVE, 'Active'),
    (PERIODICALLY_ACTIVE, 'Periodically active'),
    (ON_HOLD, 'On hold'),
    (ABANDONED, 'Abandonded'),
]

# Define the options if a project is public
# Defined here as used in more than one model
VISIBILTIY_CHOICES = [
    ('PUBLIC', 'Public'),
    ('PRIVATE', 'Private')
]

# Choices if a project would like to be included in the Metadata exchange
# Defined here as used in more than one model
SHARING_CHOICES = [
    ('DISABLED', ''),
    ('EXCHANGE', ''), # Default
]

# Defined here as used in more than one model
UN_REGIONS_CHOICES = [
    ('ZZ', 'Not Selected'),
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
    ''' Defines the project model which are projects either of an
    approved submission or retreived from the metadata exchange API.
    '''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

<<<<<<< Updated upstream
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
=======

    aim = models.CharField(
        help_text=_('Primary focus of the project.'),
        db_index=True,
        max_length=200,
        default='',
        blank=False,
        )
    description = models.CharField(
        max_length=5000,
        default=_('No description provided'),
        blank=False,
        )
    name = models.CharField(
        help_text=_('Common name for the project.'),
        db_index=True,
        max_length=200,
        blank=False,
        )
    start_date = models.DateTimeField(
        help_text=_('Date the project started.'),
        db_index=True,
        null=True,
        )
    end_date = models.DateTimeField(
        help_text=_('Date the project concluded.'),
        null=True,
        )
    status = models.CharField(
        db_index=True,
        max_length=30,
        default='0',
        choices=STATUS_CHOICES,
        )
    image_dir = models.CharField(
        max_length= 200,
        default= '',
        )
    #image_dir = 'http://localhost:8000/media/images/wild-otter-mom-and-pup_d-large.max-165x165.jpg' #TODO replace with FileField
    #image_proj_main = FileField(
        #upload_to=None,
        #max_length=100,
        #**options,
        #)
    target_audience = models.CharField(
        db_index=True, help_text=_('Project primary audience.'),
        max_length=5000,
        default='',
        )
    contact_name = models.CharField(
        help_text=_('Name of the person maintaining this entry.'),
        max_length=200,
        default='Not Provided',
        blank=True,
        )
    contact_role = models.CharField(
        help_text=_('Maintainer’s role or position with this project.'),
        max_length=200,
        default='Not Provided',
        blank=True,
        )
    contact_affiliation = models.CharField( # This is the field presented in the inial form to collect a string to try and resolve semantically, but if not found allows saving the original string too.
        help_text=_('Maintainer’s institutional affiliation.'),
        max_length=200,
        default='',
        )
    # contact_affiliation_semantic = models.ManyToManyField(Organizaiton)
    contact_email = models.CharField(
        max_length=200,
        default='',
        )
    contact_phone = models.CharField(
        max_length=200,
        default='',
        )
>>>>>>> Stashed changes
    keywords = models.ManyToManyField(Keyword)

    search_fields = ['name','description']

    # keywords
    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('projects:project_list')

    def __str__(self):
        return self.name

class ProjectSubmission(models.Model):
    ''' Defines the project model where an initial submission for a project project can be captured for
    a lead and review, but which at the time does not meet the necessary minimum or the workflow. This does not inherit field that are common with the
    project model, but will be handed off to the project form once the user recieves an approval. This may be implemented as a public form without
    a user account thus we do not want to spam inserted to the main project model stores.'''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project Submission')
        verbose_name_plural = _('Project Submissions')

    # The ordering follows the form order logic
    name = models.CharField(
        help_text=_('Common name for the project.'),
        max_length=200,
        default='',
        )
    description = models.CharField(
        max_length=5000,
        default='',
        )
    aim = models.CharField(
        help_text=_('Primary focus of the project.'),
        max_length=200, default='',
        )
    start_date = models.DateTimeField(
        help_text=_('Date the project started.'),
        null=True,
        )
    status = models.CharField(
        max_length=30,
        default='0',
        choices=STATUS_CHOICES)
    target_audience = models.CharField(
        help_text=_('Project primary audience.'),
        max_length=5000,
        default='',
        )
    contact_name = models.CharField(
        help_text=_('Name of the person maintaining this entry. Default is your account.'),
        max_length=200,
        default='',
        )
    contact_role = models.CharField(
        help_text=_('Maintainer’s role or position with this project.'),
        max_length=200,
        default='',
        )
    contact_affiliation = models.CharField(
        help_text=_('Maintainer’s institutional affiliation.'),
        max_length=200,
        default='',
        )
    contact_email = models.CharField(
        max_length=200,
        default='',
        )

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
