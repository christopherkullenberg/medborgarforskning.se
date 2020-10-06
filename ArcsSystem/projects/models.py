from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# from django_countries.fields import CountryField
from django.contrib.auth.models import User
import uuid
import os
from users.models import CustomUser

# Define the options for the state of operation a project might be classified
# Defined here as used in more than one model
STATUS_CHOICES = [
    ('0', 'Not Selected'),
    ('1', 'Not yet started'),
    ('2', 'Active'),
    ('3', 'Periodically active'),
    ('4', 'On hold'),
    ('5', 'Abandonded')
]

# Define the options if a project is public
# Defined here as used in more than one model
#VISIBILTIY_CHOICES = [
#    ('PUBLIC', 'Public'),
#    ('PRIVATE', 'Private')
#]

# Choices if a project would like to be included in the Metadata exchange
# Defined here as used in more than one model
SHARING_CHOICES = [
    ('DISABLED', 'Not Shared'),
    #('LIMITED', 'Sharing Limited') #TODO enhancement Unlikly, but available if required to trigger check for list of authorized exchanges
    ('EXCHANGE', 'Sharing'), # Default
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

class ScienceType(models.Model):
    '''Science Types for the projects'''
    class Meta:
        verbose_name = _('Science Type')
        verbose_name_plural = _('Science Types')

    ScienceType = models.TextField()

    def __str__(self):
        return f'{self.ScienceType}'

class OriginDatabase(models.Model):
    class Meta:
        verbose_name = _('Origin Database')
        verbose_name_plural = _('Origin Databases')

    originDatabase = models.TextField()

    def __str__(self):
        return f'{self.originDatabase}'

class FundingBody(models.Model):
    class Meta:
        verbose_name = _('Funding Body')
        verbose_name_plural = _('Funding Bodies')

    body = models.TextField()

    def __str__(self):
        return f'{self.body}'

class Topic(models.Model):
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    topic = models.TextField()

    def __str__(self):
        return f'{self.topic}'

class Project(models.Model):
    ''' Defines the project model which are projects either of an
    approved submission or retreived from the metadata exchange API.
    '''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        abstract = True

    '''PPSR PMM Required fields'''
    #program_campaign = models.CharField(help_text=_('Overarching group for the project.'), db_index=True, max_length=200, blank=False,)
    #projectId = CharField(help_text=_('Global Unique ID for the project.'), db_index=True, max_length=200, blank=False,) # This should be system generated by the originating platform.
    date_created = models.DateTimeField(_('The date the Project created'), auto_now=True) ## maps to PPSR PMM  projectDateCreated
    date_updated = models.DateTimeField(_('Last date the Project was updated'), auto_now=True) ## maps to PPSR PMM  projectLastUpdatedDate
    name = models.CharField(help_text=_('Common name for the project.'), db_index=True, max_length=200, blank=False,) ## maps to PPSR PMM  PMM projectName
    aim = models.CharField(help_text=_('Primary focus of the project.'), db_index=True, max_length=200, default='', blank=False,) ## maps to PPSR PMM  projectAim
    description = models.CharField(max_length=5000, default=_(''), blank=False,) ## maps to PPSR PMM  projectDescription
    #status = models.ForeignKey(Status, on_delete=models.CASCADE)
    status = models.CharField(db_index=True, max_length=30, default='0', choices=STATUS_CHOICES,) ## maps to PPSR PMM  projectStatus
    start_date = models.DateTimeField(help_text=_('Date the project started.'), db_index=True, null=True,) ## maps to PPSR PMM  projectStartDate
    #duration = models.CharField(max_length=30, default='0',) ## maps to PPSR PMM projectDuration - value should be calculated as diff from start to end or if started and no end - infinit
    science_type = models.ManyToManyField(ScienceType) ## maps to PPSR PMM projectScienceType

    '''PPSR PMM Optional Fields'''
    # has_tag = ## maps to PPSR PMM hasTag
    #difficulty_level = ## maps to PPSR PMM difficultyLevel
    keywords = models.ManyToManyField(Keyword, blank=True) ## maps to PPSR PMM keyword
    end_date = models.DateTimeField(help_text=_('Date the project ended.'), db_index=True, null=True, ) ## maps to PPSR PMM projectEndDate


    url = models.URLField(max_length=500) ## maps to PPSR PMM projectUrl
    #un_regions = ## maps to PPSR PMM unRegions
    #language = ## maps to PPSR PMM language - language encoding of the record

    #locality_text = models.CharField(blank=True,) ## maps to PPSR PMM projectLocality
    responsible_party_name = models.CharField(blank=True, max_length=50,) ## maps to PPSR PMM projectResponsiblePartyName
    responsible_party_email = models.CharField(blank=True, max_length=50,) ## maps to PPSR PMM projectResponsiblePartyContactEmail

    #contactPoint ## maps to PPSR PMM contactPoint - vocabulary not yet finalized by PPSR group
    contact_name = models.CharField(help_text=_('Name of the person maintaining this entry.'),max_length=200,default='Not Provided', blank=True,) ## maps to PPSR PMM contactName

    #PPSR PMM meansOfContact - controlled vocabulary list ie (email, phone, website, physical address)
    contact_role = models.CharField(help_text=_('Maintainer’s role or position with this project.'), max_length=200, default='Not Provided', blank=True,)
    contact_affiliation = models.CharField(help_text =_('Maintainer’s institutional affiliation.'), max_length=200, default='',) # This is the field presented in the inial form to collect a string to try and resolve semantically, but if not found allows saving the original string too.
    # contact_affiliation_semantic = models.ManyToManyField(Organizaiton)
    contact_email = models.CharField(max_length=200, default='',)
    contact_phone = models.CharField(max_length=200, default='',)
    target_audience = models.CharField(db_index=True, help_text=_('Project primary audience.'), max_length=5000, default='',)
    #origin = models.CharField(max_length=100)
    image_dir = models.CharField(max_length= 200,default= '',)
    #image_proj_main = FileField(upload_to=None, max_length=100, **options,)
    #image_proj_main_credit = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9,decimal_places=6, blank=True, null=True) ## maps to PPSR PMM projectPinLatitude
    longitude = models.DecimalField(max_digits=9,decimal_places=6, blank=True, null=True) ## maps to PPSR PMM projectPinLongitude
    # ## maps to PPSR PMM projectGeographicCoverage - geoObject
    # coverage_latitude = models.DecimalField(max_digits=9,decimal_places=6) ## maps to PPSR PMM projectGeographicCoverageCentroidLatitude
    # coverage_longitude = models.DecimalField(max_digits=9,decimal_places=6)# ## maps to PPSR PMM projectGeographicCoverageCentroidLongitude
    # country = CountryField()

    #activity =
    #how_to_participate = models.CharField(max_length=2000)
    #equipment = models.CharField(max_length=2000)

    '''ARCSCore Additional Fields'''
    #languages_supported = # The languages that the project officially supports in iso - sv, no, etc
    exchanged = models.CharField(max_length=30, default='0', choices=SHARING_CHOICES,)
    featured = models.BooleanField(null=True, blank=True) # Activate display of project in feature locations - ie homepage slider or other using this flag

    '''temporary notes'''
    #contactDetails
    #contactPointType

    #projectMedia
    #projectMediaType
    #projectMediaFile
    #projectMediaCredit

    #projectGeographicLocation
    #projectPinLatitude
    #projectPinLongitude
    #projectGeographicCoverage
    #projectGeographicCoverageCentroidLatitude
    #projectGeographicCoverageCentroidLongitude
    #activity
    #projectExternalId
    #cosi:belongsToProgramme
    #projectOriginalRepository
    #projectHowToParticipate
    #projectTask
    #projectIntendedOutcomes
    #projectOutcome
    #scientificProcessInvolved
    #numberOfScientificPublications
    #numberOfOtherPublications
    #projectAdditionalInformation
    #projectCountry
    #projectEquipment
    #projectExternalLinks
    #projectPlannedEndDate
    #projectPlannedStartDate
    #projectResearchType
    #projectScientificCollaborators
    #projectAssociatedParty
    #projectAssociatedPartyId
    #projectAssociatedPartyName
    #projectUsFederalSponsor
    #projectAssociatedPartyRole
    #participationFees
    #participationFeeApplicable
    #participationFeeAmount
    #projectFunding
    #projectFundingSource
    #projectFundingSourcePercentageAmount
    #projectFundingSourceCurrencyAmount
    #projectFundingSourceType
    #fundingSourceTypeSubsetA
    #fundingSourceTypeSubsetB
    #projectParticipants
    #projectParticipantsNumberOfActive
    #projectParticipantsTotalRegistered
    #projectParticipantAge

    #creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #author = models.CharField(max_length=100, null=True, blank=True)
    #author_email =  models.CharField(max_length=100)
    #host = models.CharField(max_length=200)
    #fundingBody = models.ForeignKey(FundingBody, on_delete=models.CASCADE,null=True, blank=True)
    #fundingProgram = models.CharField(max_length=500)
    #originDatabase = models.ForeignKey(OriginDatabase, on_delete=models.CASCADE,null=True, blank=True)
    #originURL = models.CharField(max_length=200)
    #originUID = models.CharField(max_length=200)
    '''end temporary notes'''



    # This is to get the user 



    search_fields = ['name','description']

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True )
    #lable = 'Upload image',  help_text = 'Choose an image that will in one picure decribe your project'
    image = models.ImageField(null=True, blank=True, upload_to="project_images")




    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('projects:project_list')

    def create_project_platform_UUID():
        # Global UUID by for ARCSCore
        return 'ARCS' + str(uuid.uuid4) # TODO consider replacing ARCS string with configurable string for namespacing

    def get_status_name(self):
        return STATUS_CHOICES[int(self.status)][1]



    def __str__(self):
        return self.name


class ProjectEntry(Project):
    ''' Extends the Project model to capture the additional fields for a project project that has
    been approved for adding to the database and may be included in the API exchange '''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project Entry')
        verbose_name_plural = _('Project Entries')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('projects:project_list')

    def get_absolute_url_details(self):
        return reverse('projects:project_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class ProjectSubmission(Project):
    ''' Extends the Project model for an lead submissions about a potential project that needs review and extending to be added to the database
    for exchange. Once approved it will be moved to the ProjectEntry model and will be available in the shared database.
    We do not want spam inserted to the main project model stores and can enforce fields differently than a Projectentry.'''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project Submission')
        verbose_name_plural = _('Project Submissions')

    # The ordering follows the form order logic

    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('projects:project_list')

    def get_absolute_url_details(self):
        return reverse('projects:project_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class ProjectExternal(Project):
    ''' Extends the Project model for entries that are from external databases.'''

    class Meta:
        # Explicit add of names and plurals instead of relying on model name fallback
        # https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#model-verbose-names-values
        verbose_name = _('Project External')
        verbose_name_plural = _('Project External')


    def __str__(self):
        return self.name
