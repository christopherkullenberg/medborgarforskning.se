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

    title = models.CharField(
        max_length=200,
        default="title",
        )
    keywords = models.ManyToManyField(Keyword)
    abstract = models.CharField(
        max_length=5000,
        default=_('Empty'),
        )
    doi = models.CharField(
        help_text=_("DOI without http"),
        max_length=200,
        blank=True,
        ) # format like 10.1016/J.BIOCON.2016.05.015
    py = models.IntegerField(
        help_text=_("Publication Year - YYYY"),
        default="0000",
        ) #Todo make variable semantic - move to PubYear
    authors = models.CharField(
        help_text=_("Author String"),
        max_length=500,
        default=_("Author"),
        ) # ['author1','author2','author3...etc']
    # authors_sementic = # TODO add field to resolved authors to ORCID ['authorWikidataID1','','authorWikidataID3']
    source = models.CharField(
        help_text=_("Source Name"),
        max_length=200,
        blank=True,
        )
    volume = models.CharField(
        help_text=_("Volume"),
        max_length=200,
        blank=True,
        )
    issue = models.CharField(
        help_text=_("Issue Number"),
        max_length=200,
        blank=True,
        )
    # wikidataID = models.CharField(
    #     max_length=200,
    #     blank=True
    #     ) # formate of Q56417560

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
