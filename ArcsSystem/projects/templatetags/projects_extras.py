

from django import template
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe


register = template.Library()



def get_keywords(string):

    if string == "swe":

        return [k.keyword for k in KeywordSwe.objects.all()]

    if string == "eng":

        return [k.keyword for k in KeywordEng.objects.all()]

    return []




register.filter("get_keywords", get_keywords)