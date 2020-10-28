from django.db import models
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.urls import path,reverse
from projects.models import KeywordSwe, KeywordEng, KeywordLine


class WorkPackage(models.Model):
    '''
    '''
    class Meta:
        verbose_name = _('Work package')
        verbose_name_plural = _('Work packages')

    name = models.CharField(max_length=300, null=False)
    introduction = models.TextField()
    detailed_content = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('workpackages:category_view',
                       kwargs={'category' : self.id}
                       )


class Theme(models.Model):
    '''
    '''
    class Meta:
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')
    title = models.CharField(max_length=300, null=False)
    body = models.TextField()
    related_papers_tags = TaggableManager()
    related_publications = models.CharField(max_length=1000, blank=True, null=False)
    wp_parent = models.ForeignKey(WorkPackage,
                                  default=1,
                                  verbose_name="Work Package",
                                  on_delete=models.SET_DEFAULT)


    keyword_lines = models.ManyToManyField(KeywordLine, related_name="Theme", blank=True)

    def get_pub_ids(self):

        return self.related_publications.split("&")[:-1]

    def save_pub_ids(self, li):

        string = ""
        for el in li:
            string += el + "&"
        self.related_publications = string
        self.save()

    def get_absolute_url(self):
        # reverse expects the view name
        return reverse('workpackages:theme_view',
                       kwargs={'category' : self.id}
                       )

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
                            ''' + '''  <button style="height:100px; color :white; font-size: 10px" class=" col project-items-justify form-control blackFieldWhiteText" type="button" onclick="location.href=' '''+ self.get_absolute_url() + '''  ';"  />
                            ''' + limit_string(self.wp_parent.name,limit) + ": <br> " +  self.title +   ''' </button>  ''' +  '''
                        </div>
                    </div>

                    <div class="col" style="padding-right: 5px; padding-left: 5px; margin-top: 3px">

                        <div class="row Lato-font ">
                            <div class="col" >
                                <span  >  
                                ''' + limit_string(self.body, limit) +  ''' 
                                </span>
                            </div>
                        </div>
                        <hr>

                        '''

        kw_limit = 9

        if use == "all":

            for line in self.keyword_lines.all()[:kw_limit]:
                html += ''' <span style="color:black;"> '''+ line.eng.keyword + '''</span> <br> '''
        else:

            kl = self.keyword_lines.filter(eng__id__in=use)[:kw_limit]

            print(use)

            print(kl)
            print([test_x.eng.id for test_x in kl])

            count = 0

            for line in kl:
                html += ''' <span style="color:red;"> '''+ line.eng.keyword + '''</span> <br> '''
                count +=1

            if count < kw_limit:

                for line in self.keyword_lines.all().exclude(eng__id__in=kl)[:kw_limit- count]:
                    html += ''' <span style="color:black;"> '''+line.eng.keyword + '''</span> <br> '''
        html += '''</div>
            </div>
        </div>'''

        return html






    def __str__(self):
        return f'{self.title}'


def limit_string(string, limit):

    if len(string) <= limit:
        return string
    else:
        return string[:limit-3] + "..." 


