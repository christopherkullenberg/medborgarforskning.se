from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    pass
    # add additional fields for users here, extends core Django User
    # add additional fields in here

    def __str__(self):
        return self.username
