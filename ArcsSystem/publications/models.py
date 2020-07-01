from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Keyword(models.Model):
    '''
    '''
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

    keyword = models.TextField()
    def __str__(self):
        return f'{self.keyword}'


#class Publication(models.Model):
#    '''
#    '''
#    class Meta:
#        verbose_name = _('Publication')
#        verbose_name_plural = _('Publications')
#
#    title = models.CharField(max_length=200)
#    keywords = models.ManyToManyField(Keyword)
#    abstract = models.CharField(max_length=5000, default=_('Empty'))
#
#    def __str__(self):
#        return self.title


class Article(models.Model):
    ''' Defines minimal fields necessary to hold a peer reviewed article
    '''
    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
    title = models.CharField(max_length=200, default="title")
    keywords = models.ManyToManyField(Keyword)
    abstract = models.CharField(max_length=5000, default=_('Empty'))
    doi = models.CharField(max_length=200, default=_("doi"))
    py = models.IntegerField(default="0")
    authors = models.CharField(max_length=500, default=_("Author"))
    source = models.CharField(max_length=200, default=_("Journal Name"))
    volume = models.CharField(max_length=200, default=_("Volume"))
    issue = models.CharField(max_length=200, default=_("Issue"))


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publications:article_publications_detail', args=[str(self.id)])


#class Arcsreport(Publication):
#    '''
#    '''
#    class Meta:
#        verbose_name = _('Arcs Report')
#        verbose_name_plural = _('Arcs Reports')
#
#    def __str__(self):
#        return self.title
