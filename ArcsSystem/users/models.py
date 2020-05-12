from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    '''Initialized a custom user model referencing a django standard user model 1:1'''
    pass
    # add additional fields for users here, extends core Django User
    # add additional fields in here

    def __str__(self):
        return self.username
