from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.
class Organization(models.Model):
    '''Defines the model for organizaitons referenced as the affiliation of
    users, projects, and groups.'''

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    name = models.CharField(
        max_length=200,
        ) # String of default language label
    wikidataID = models.CharField(
        max_length=200,
        ) # Format should be Q followed by numerics only - optional field, but helps enrich queries - Example University of Gothenburg is Q371522
    description = models.CharField(
        max_length=200,
        )
    # The following are fields that will be cached from Wikidata to provide other relevant information on the organizaiton
    website = models.CharField(
        max_length=200,
        )
    # websiteWdProperty = P856
    # websiteWdValue =
    # SwedishOrgNumberWDProperty = "P6460"  # Q6460 - Swedish Organization Number


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizations:organization_detail', args=[str(self.id)])
