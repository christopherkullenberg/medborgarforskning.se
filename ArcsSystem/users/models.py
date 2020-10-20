from django.contrib.auth.models import AbstractUser
from django.urls import path,reverse
from django.db import models
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    '''Initialized a custom user model that extends the current user model'''
    # django built in default model fields - https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
    ## username # this is built into the User Model set at account creation
    ## first_name # this is built into the User Model set at account creation
    ## last_name # this is built into the User Model set at account creation
    ## email # this is built into the User Model set at account creation
    ## password # this is built into the User Model set at account creation
    ## groups # this is built into the User Model set at account creation
    ## user_permissions # this is built into the User Model set at account creation
    ## is_staff # this is built into the User Model, this is initialized at account creation - default False
    ## is_active # this is built into the User Model.. this is set at account creation
    ## is_superuser # this is set at account creation
    ## last_login # this is set at account creation
    ## date_joined # this is set at account creation

    # Fields extending the base user model that should not be used publicly
    ## Fields for compliance

    accepted_eula = models.BooleanField(default=False, editable=False)
    accepted_eula_version = models.CharField(max_length=25, blank=False, null=True)
    accepted_eula_date = models.DateField(auto_now_add=True, null=True) #TODO compare to date TOS was updated to ensure notice is presented that the terms changed.

    username = models.SlugField(max_length=50, unique=True)

    # Fields extending the base user model that may be used publicly is a unique ID
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    orcid = models.CharField("ORCID", max_length=50, blank=True, null=True) # TODO add when AllAuth ORCID login is used.
    # highlihgted papers = # TODO query list of papers in ORCID to select and display

    # Information about the User
    # language_native =
    # language_competency = # selection of language
    title = models.CharField("Title", max_length=200, blank=True, null=True)
    bio_general = models.CharField("Short Intro Biography", max_length=500, blank=True, null=True)
    bio_research_interest = models.CharField("Short Outline of your Interests", max_length=500, blank=True, null=True)
    connections = models.CharField("Describe the connections and/or collaboration you are seeking.", max_length=400, blank=True, null=True)
    personal_website_address = models.CharField("Other personal website adress", max_length=200, blank=True, null=True)
    institution = models.CharField("Institution", max_length=200, blank=True, null=True)

    #affiliation = # TODO link with organizations app #TODO allow selecting projects to show affiliation (projects,etc)

    # Research

    #location_zipcode = models.CharField("ZIP / Postal code", max_length=12, blank=True) # by zip code granularity to find those nearby? #TODO validate format
    # creattion_date = models.DateField(null=True, blank=True)


    # add additional fields for users here, extends core Django User
    def __str__(self):
        return self.username

    def get_first_name(self):
        return self.first_name

    def get_absolute_url(self):
        # reverse expects the view name
        a = reverse('userprofile_public_view',
                        kwargs={'slug': self.username})
        return a

class InterestArea(models.Model):
    interestArea = models.TextField()
    def __str__(self):
        return f'{self.interestArea}'
