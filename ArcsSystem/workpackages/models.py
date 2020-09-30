from django.db import models
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse


class WorkPackage(models.Model):
    '''
    '''
    class Meta:
        verbose_name = _('Work package')
        verbose_name_plural = _('Work packages')

    name = models.SlugField()
    introduction = models.TextField()
    detailed_content = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('workpackages:category_view',
                       kwargs={'category' : self.name}
                       )


class Theme(models.Model):
    '''
    '''
    class Meta:
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')
    title = models.SlugField()
    body = models.TextField()
    related_papers_tags = TaggableManager()
    related_publications = models.CharField(max_length=1000, blank=True, null=False)
    wp_parent = models.ForeignKey(WorkPackage,
                                  default=1,
                                  verbose_name="Work Package",
                                  on_delete=models.SET_DEFAULT)

    def get_pub_ids(self):

        return self.related_publications.split("&")[:-1]

    def save_pub_ids(self, li):

        string = ""
        for el in li:
            string += el + "&"
        self.related_publications = string
        self.save()





    def __str__(self):
        return f'{self.title}'
