from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from projects.models import KeywordEng


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
        max_length=20000,
        default="title",
        )
    keywords = models.ManyToManyField(KeywordEng, related_name="Article")
    abstract = models.CharField(
        max_length=50000,
        default=_('Empty'),
        )
    doi = models.CharField(
        help_text=_("DOI without http"),
        max_length=20000,
        blank=True,
        ) # format like 10.1016/J.BIOCON.2016.05.015
    py = models.IntegerField(
        help_text=_("Publication Year - YYYY"),
        default="0000",
        ) #Todo make variable semantic - move to PubYear
    authors = models.CharField(
        help_text=_("Author String"),
        max_length=50000,
        default=_("Author"),
        ) # ['author1','author2','author3...etc']
    # authors_sementic = # TODO add field to resolved authors to ORCID ['authorWikidataID1','','authorWikidataID3']
    source = models.CharField(
        help_text=_("Source Name"),
        max_length=20000,
        blank=True,
        )
    volume = models.CharField(
        help_text=_("Volume"),
        max_length=20000,
        blank=True,
        )
    issue = models.CharField(
        help_text=_("Issue Number"),
        max_length=20000,
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



    def get_custom_html(self, lang="en", use ="all"):

        limit = 60

        di = {}
        di["en"] = []
        di["sv"] = []

        #return "<div class='col-4' > <a href='" + self.get_absolute_url_details() +   "'>" + self.name +  "</a> </div>"
        html =   '''
            <div style="padding-left: 20px; padding-right: 20px; font-size:10px" class="col-lg-3 col-md-4 col-xs-6 mb-5">
                <div class="project-item">
                    <div class="row">
                        <div class=" col">
                            ''' + '''  <button style="height:100px; color :white; font-size: 10px" class=" col project-items-justify form-control blackFieldWhiteText" type="button" onclick="location.href=' '''+ self.get_absolute_url() + '''  ';"  /> ''' +  self.title +  ''' </button>  ''' +  '''
                        </div>
                    </div>

                    <div class="col" style="padding-right: 5px; padding-left: 5px; margin-top: 3px">

                        <div class="row Lato-font ">
                            <div class="col" >
                                <span  >

                                ''' + limit_string(self.authors,limit) + " "  + str( self.py) + " " + limit_string(self.source, limit) + " " + self.volume + "("+ self.issue +")"+  '''

                                </span>
                            </div>
                        </div>
                        <hr>


                        <div class="row Lato-font ">
                            <div class="col" >
                                <a href="https://doi.org/''' + self.doi +  '''" > Get full article </a>
                            </div>
                        </div>
                        <hr>

                        '''

        kw_limit = 9

        if use == "all":

            for key in self.keywords.all()[:kw_limit]:
                html += ''' <span style="color:black;"> '''+ key.keyword + '''</span> <br> '''
        else:

            kl = self.keywords.filter(id__in=use)[:kw_limit]

            count = 0

            for key in kl:
                html += ''' <span style="color:red;"> '''+ key.keyword + '''</span> <br> '''
                count +=1

            if count < kw_limit:

                for key in self.keywords.all().exclude(id__in=kl)[:kw_limit- count]:
                    html += ''' <span style="color:black;"> '''+ key.keyword + '''</span> <br> '''
        html += '''</div>
            </div>
        </div>'''

        return html


#class Arcsreport(Publication):
#    '''
#    '''
#    class Meta:
#        verbose_name = _('Arcs Report')
#        verbose_name_plural = _('Arcs Reports')
#
#    def __str__(self):
#        return self.title


def limit_string(string, limit):

    if len(string) <= limit:
        return string
    else:
        return string[:limit-3] + "..."
