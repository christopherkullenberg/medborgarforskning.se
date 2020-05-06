from django.db import models



class Keyword(models.Model):
    '''
    '''
    keyword = models.TextField()
    def __str__(self):
        return f'{self.keyword}'


class Publication(models.Model):
    '''
    '''
    title = models.CharField(max_length=200)
    keywords = models.ManyToManyField(Keyword)
    abstract = models.CharField(max_length=5000, default='Empty')

    def __str__(self):
        return self.title


class Article(Publication):
    '''
    '''
    doi = models.CharField(max_length=200, default="doi")
    py = models.IntegerField(default="0")
    authors = models.CharField(max_length=500, default="Author")
    source = models.CharField(max_length=200, default="Journal Name")
    volume = models.CharField(max_length=200, default="Volume")
    issue = models.CharField(max_length=200, default="Issue")


    def __str__(self):
        return self.title


class Arcsreport(Publication):
    '''
    '''

    def __str__(self):
        return self.title
