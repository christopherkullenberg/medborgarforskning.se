from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from organizations.models import Organization
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    '''Initialized a custom user model that extends the current user model'''
    # django built in default model fields
    ## username # this is set at account creation
    ## email # this is set at account creation

    # Fields that may be used publicly in profile
    #bio = models.TextField(max_length=500, blank=True)
    #location = models.CharField(max_length=30, blank=True)
    # affiliations
    # creattion_date = models.DateField(null=True, blank=True)
    # add additional fields for users here, extends core Django User
    slug = models.UUIDField(
        default=uuid.uuid4,
        blank=True,
        editable=False
        ) # Unique ID for the user
    orcid = models.CharField(
        help_text=_('ORCID'),
        max_length=50,
        blank=True,
        ) # Retreieved from login with ORCID or linking to user account via Oauth - TODO make clear in consent the use to link to Wikidata and publicaitons
    wikidataID = models.CharField(
        help_text=_('Wikidata Q Identifier for publicaiton authors with matching ORCID'),
        max_length=50,
        blank=True,
        ) # Matched on ORCID if provided to link to publications graph on Wikidata - TODO add to consent of user account.
    title = models.CharField(
        max_length=200,
        blank=True,
        )
    bio = models.CharField(
        help_text=_('Primary focus of the project.'),
        max_length=400,
        blank=True,
        ) # Displayed on user profile a descri
    # project_affiliation = models.ManyToManyField(Project, blank=True) foreign key to project indicating the user states they are part of a project
    org_affiliation = models.ManyToManyField(Organization, blank=True) # foreign key foreign key to org which the user states they are part of


    def __str__(self):
        return self.username
