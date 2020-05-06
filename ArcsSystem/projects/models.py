from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse

STATUS_CHOICES = [
    ('0', 'Not yet started'),
    ('1', 'Active'),
    ('2', 'Periodically active'),
    ('3', 'On hold'),
    ('4', 'Abandonded')
]

VISIBILTIY_CHOICES = [
    ('H', 'Hidden'),
    ('V', 'Visible')
]

UN_REGIONS_CHOICES = [
    ('AF', 'Africa'),
    ('SA', 'Americas-South America'),
    ('CA', 'Americas-Central America'),
    ('NA', 'Americas-North America'),
    ('AS', 'Asia'),
    ('EU', 'Europe'),
    ('OC', 'Oceana')
]

class Keyword(models.Model):
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
    start_date = models.DateTimeField(help_text=_('Date the project started.'),blank=True)
    end_date = models.DateTimeField(help_text=_('Date the project concluded.'),blank=True)
    status = models.CharField(max_length=30, default='Empty', choices=STATUS_CHOICES)
    #status = models.CharField(max_length=30, default='Empty')
    image_dir = 'http://localhost:8000/media/images/wild-otter-mom-and-pup_d-large.max-165x165.jpg'
    target_audience = models.CharField(help_text=_('Project primary audience.'),max_length=5000, default='')
    contact_name = models.CharField(help_text=_('Name of the person maintaining this entry. Default is your account.'),max_length=200, default='')
    contact_role = models.CharField(help_text=_('Maintainer’s role or position with this project.'),max_length=200, default='')
    contact_affiliation = models.CharField(help_text=_('Maintainer’s institutional affiliation.'),max_length=200, default='')
    contact_email = models.CharField(max_length=200, default='')
    contact_phone = models.CharField(max_length=200, default='')
    keywords = models.ManyToManyField(Keyword)

    # keywords
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={'pk': self.id})

    def __str__(self):
        return self.name
