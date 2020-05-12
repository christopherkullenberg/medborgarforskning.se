from django.db import models
from taggit.managers import TaggableManager


class WorkPackage(models.Model):
    name = models.TextField()
    introduction = models.TextField()
    detailed_content = models.TextField()

    def __str__(self):
        return self.title


class Theme(models.Model):
    title = models.TextField()
    body = models.TextField()
    related_papers_tags = TaggableManager()
    wp_parent = models.ForeignKey(WorkPackage,
                                  default=1,
                                  verbose_name="Work Package",
                                  on_delete=models.SET_DEFAULT))

    def __str__(self):
        return f'{self.title}'
