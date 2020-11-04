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
from organizations.models import Organization

from wikidata.client import Client

# Define the options for the state of operation a project might be classified
# Defined here as used in more than one model
STATUS_CHOICES = [
    ('0', 'Not Selected'),
    ('1', 'Not yet started'),
    ('2', 'Active'),
    ('3', 'Periodically active'),
    ('4', 'On hold'),
    ('5', 'Completed'),
    ('6', 'Abandonded')
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






class KeywordSwe(models.Model):
    '''Keywords for the projects'''
    class Meta:
        verbose_name = _('Keyword_sv')
        verbose_name_plural = _('Keywords_sv')

    keyword = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return f'{self.keyword}'

class KeywordEng(models.Model):
    '''Keywords for the projects'''
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')


    summary_en = models.CharField(blank=True, null=True, max_length = 20000,)
    summary_sv = models.CharField(blank=True, null=True, max_length = 20000,)
    wikidataQ = models.IntegerField(blank=True, null=True)

    keyword = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return f'{self.keyword}'

    def get_absolute_url(self):
        return reverse('keywords:keyword_detail', args=[str(self.keyword)])

    def get_custom_html(self):
        return ''' <a href="'''+ self.get_absolute_url()+'''">'''+ self.keyword + ''' </a> '''

    def get_wikidataQ(self):

        if self.wikidataQ != None:

            html = '''<hr> <br> <br>  Source:  <a href="https://wikidata.org/wiki/Q''' +str(self.wikidataQ) +'''" >Wikidata entry</a>  <br> <br> '''
            html += ''' <div class="row" >'''

            cl = Client()

            ent = cl.get("Q" + str(self.wikidataQ), load=True)

            # first col
            html += ''' <div class"col-6">    <h5>  '''+ str(ent.description) +''' </h5>  '''



            # image
            if "P18" in ent.data["claims"]:
                prop = cl.get("P18")
                thing = ent[prop]
                html += ''' <img style="width:400px;heigth:400px" src="'''+ thing.image_url +'''" alt=""> '''
            html += ''' </div> '''
            # end first col

            if "P225" in ent.data["claims"]:
                prop = cl.get("P225")
                thing = ent[prop]
                html += ''' <div class="col-4" style="margin-left:40px" >  <h5> Taxon name: '''+ thing +''' </h5> </div> '''

            html += ''' </div>  '''
            return html
        return ""



    def get_summary(self, lang="en"):
        if lang == "en":
            use = self.summary_en
        if lang == "sv":
            use = self.summary_sv

        if use != None:
            return use + '''<br> <br> <p style="font-size:20px;">Source: <a href="https://en.wikipedia.org/wiki/''' + self.keyword +'''" >Wikipedia</a></p>'''
        return "<p> No short description found </p>"






    # def get_custom_html(self):





class KeywordLine(models.Model):

    swe = models.ForeignKey(KeywordSwe, on_delete=models.SET_NULL, blank=True, null=True, related_name='line' )
    eng = models.ForeignKey(KeywordEng, on_delete=models.SET_NULL, blank=True, null=True, related_name='line' )

    def get_line(self):

        if self.swe == None:
            swe = ""
        else:
            swe = self.swe.keyword

        if self.eng == None:
            eng = ""
        else:
            eng = self.eng.keyword
        return [swe, eng]

    def get_singel_kw_obj(self, lang):


        if lang == "sv":
            if self.swe != None:
                return self.swe
            return self.eng
        if lang == "en":
            if self.eng != None:
                return self.eng
            return self.swe

    def get_singel_kw(self, lang):
        return self.get_singel_kw_obj(lang).keyword



    def get_custom_html(self):

        if self.eng != None:
            return self.eng.get_custom_html()
        return ""





    def __str__(self):

        if self.eng == None:
            return f'{self.swe.keyword}'

        if self.swe == None:
            return f'{self.eng.keyword}'
        return f'{self.swe.keyword + " | " + self.eng.keyword}'

    # def get_custom_html(self, lang="en"):

    #     if lang == "sv":
    #         return [KeywordLine.objects.get(id=int(pk)).swe.keyword if KeywordLine.objects.get(id=int(pk)).swe is not None else KeywordLine.objects.get(id=int(pk)).eng.keyword for pk in  self.keywords.split("&")[:-1] ]
    #     if lang == "en":
    #         return [KeywordLine.objects.get(id=int(pk)).eng.keyword if KeywordLine.objects.get(id=int(pk)).eng is not None else KeywordLine.objects.get(id=int(pk)).swe.keyword for pk in  self.keywords.split("&")[:-1] ]







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

    aim = models.CharField(help_text=_('Primary focus of the project.'), db_index=True, max_length=600, default='', blank=False,) ## maps to PPSR PMM  projectAim
    description = models.CharField(max_length=5000, default=_(''), blank=False,) ## maps to PPSR PMM  projectDescription
    #status = models.ForeignKey(Status, on_delete=models.CASCADE)
    status = models.CharField(db_index=True, max_length=30, default='0', choices=STATUS_CHOICES,) ## maps to PPSR PMM  projectStatus
    start_date = models.DateTimeField(help_text=_('Date the project started.'), db_index=True, null=True,) ## maps to PPSR PMM  projectStartDate
    #duration = models.CharField(max_length=30, default='0',) ## maps to PPSR PMM projectDuration - value should be calculated as diff from start to end or if started and no end - infinit
    science_type = models.ManyToManyField(ScienceType) ## maps to PPSR PMM projectScienceType
    '''PPSR PMM Optional Fields'''
    # has_tag = ## maps to PPSR PMM hasTag
    #difficulty_level = ## maps to PPSR PMM difficultyLevel
    ## maps to PPSR PMM keyword
    end_date = models.DateTimeField(help_text=_('Date the project ended.'), db_index=True, null=True, ) ## maps to PPSR PMM projectEndDate


    url = models.URLField(max_length=500, blank=True, verbose_name="Project url") ## maps to PPSR PMM projectUrl
    #un_regions = ## maps to PPSR PMM unRegions
    #language = ## maps to PPSR PMM language - language encoding of the record

    #locality_text = models.CharField(blank=True,) ## maps to PPSR PMM projectLocality
    responsible_party_name = models.CharField(blank=True, max_length=50,) ## maps to PPSR PMM projectResponsiblePartyName
    responsible_party_email = models.CharField(blank=True, max_length=50,) ## maps to PPSR PMM projectResponsiblePartyContactEmail

    #contactPoint ## maps to PPSR PMM contactPoint - vocabulary not yet finalized by PPSR group
    contact_name = models.CharField(help_text=_('Name of the person maintaining this entry.'),max_length=200,default='Not Provided', blank=True,) ## maps to PPSR PMM contactName

    #PPSR PMM meansOfContact - controlled vocabulary list ie (email, phone, website, physical address)
    contact_role = models.CharField(help_text=_('Maintainer’s role or position with this project.'), max_length=200, default='Not Provided', blank=True,)
    #contact_affiliation = models.CharField(help_text =_('Maintainer’s institutional affiliation.'), max_length=200, default='',) # This is the field presented in the inial form to collect a string to try and resolve semantically, but if not found allows saving the original string too.

    contact_affiliation = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True )
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


    #card vertion

    name_card = models.CharField(help_text=_('Common name for the project.'), db_index=True, max_length=30, blank=True, verbose_name="Short Name (30 chars)") ## maps to PPSR PMM  PMM projectName
    aim_card = models.CharField(help_text=_('Primary focus of the project.'), db_index=True, max_length=100, default='', blank=False, verbose_name="Short aim (100 chars)")  ## maps to PPSR PMM  projectAim
    description_card = models.CharField(max_length=100, default=_(''), blank=False, verbose_name="short description (100 chars)" ) ## maps to PPSR PMM  projectDescription



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

    def get_card_name(self):
        if self.name_card != "" :
            return self.name_card
        return self.name

    def get_card_image_url(self):

        if self.image:
            return self.image.url
        return ""



    def get_card_aim(self):
        if self.aim_card != "" :
            return self.aim_card
        return self.aim

    def get_card_description(self):
        if self.description_card != "" :
            return self.description_card
        return self.description


    def get_custom_html(self, lang="en", use="all"):

        di = {}
        di["en"] = []
        di["sv"] = []

        #return "<div class='col-4' > <a href='" + self.get_absolute_url_details() +   "'>" + self.name +  "</a> </div>"
        html =   '''
            <div style="padding-left: 20px; padding-right: 20px" class="col-lg-3 col-md-4 col-xs-6 mb-5">
                <div class="project-item">
                    <div class="row">
                        <div class=" col">
                            <div  class="col project-items-justify blackFieldWhiteText">
                                <h4 align="center"><a style="color: white; font-size: 16px" id="project-items-link" href= " ''' + self.get_absolute_url_details() + ''' ">  ''' + self.get_card_name() + '''</a></h4>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <img class="mg-fluid w-100" src=" ''' + self.get_card_image_url() + ''' " alt=""/>
                        </div>
                    </div>
                    <div class="col" style="padding-right: 5px; padding-left: 5px; margin-top: 3px">
                        <div class="row Lato-font ">
                            <div class="col" >
                                <span class="font-italic">PROJECT AIM: </span> <span class="font-weight-light" style=" font-size: 14px;" >  ''' +self.get_card_aim() + ''' </span>
                            </div>
                        </div>
                        <hr>
                        <div class="row Lato-font">
                            <div class="col">
                                <span >DESCRIPTION: </span> <span > ''' +self.get_card_description() + ''' </span>
                            </div>
                        </div>
                        <hr>
                        <div class="row Lato-font">
                            <div class="col ">
                                STATUS:  ''' + self.get_status_name() + '''
                            </div>
                        </div>
                        <hr>
                        '''

        for key in self.get_keywords(lang=lang):

            html += ''' <a style="color:blue"> ''' + key + ''' , </a>  '''

        html += '''</div>
            </div>
        </div>'''

        return html



    def __str__(self):
        return self.name


class ProjectEntry(Project):
    ''' Extends the Project model to capture the additional fields for a project project that has
    been approved for adding to the database and may be included in the API exchange '''

    keywords = models.CharField(blank=True, max_length=100)
    keyword_lines = models.ManyToManyField(KeywordLine, related_name="Project", blank=True)
    # keywords = models.Manytomany(KeywordLine, blank=True)

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


    def add_keyword(self, line):

        self.keywords += str(line.id) + "&"

    def get_keywords(self, lang="en"):






        if lang == "sv":
            return [KeywordLine.objects.get(id=int(pk)).swe.keyword if KeywordLine.objects.get(id=int(pk)).swe is not None else KeywordLine.objects.get(id=int(pk)).eng.keyword for pk in  self.keywords.split("&")[:-1] ]
        if lang == "en":
            return [KeywordLine.objects.get(id=int(pk)).eng.keyword if KeywordLine.objects.get(id=int(pk)).eng is not None else KeywordLine.objects.get(id=int(pk)).swe.keyword for pk in  self.keywords.split("&")[:-1] ]

    def get_sv_en_keywords(self):

        sv = []
        en = []

        for line_id in self.keywords.split("&")[:-1]:

            line = KeywordLine.objects.get(id=int(line_id))

            if line.swe == None:
                sv.append("")
            else:
                sv.append(line.swe.keyword)

            if line.eng == None:
                en.append("")
            else:
                en.append(line.eng.keyword)


        return sv, en










class ProjectSubmission(Project):
    ''' Extends the Project model for an lead submissions about a potential project that needs review and extending to be added to the database
    for exchange. Once approved it will be moved to the ProjectEntry model and will be available in the shared database.
    We do not want spam inserted to the main project model stores and can enforce fields differently than a Projectentry.'''

    keywords_sv = models.CharField(max_length=50, blank=True, null=True)
    keywords_en = models.CharField(max_length=50, blank=True, null=True)

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

    def get_keywords(self):

        if self.keywords_sv == None or self.keywords_sv == None:
            return [], []
        return self.keywords_sv.split("&")[:-1], self.keywords_en.split("&")[:-1],

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
