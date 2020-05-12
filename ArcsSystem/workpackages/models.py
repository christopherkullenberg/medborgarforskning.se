from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

class Theme(models.Model):
    title = models.TextField()
    body = models.TextField()
    related_papers_tags = TaggableManager()

    def __str__(self):
        return f'{self.title}'


class WorkPackage(models.Model):
    name = models.TextField()
    introduction = models.TextField()
    detailed_content = models.TextField()
    themes = models.ManyToManyField(Theme)
    
    def __str__(self):
        return self.title
