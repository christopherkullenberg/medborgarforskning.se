from django.contrib.auth.models import AbstractUser
from django.db import models

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
    pass

    def __str__(self):
        return self.username
