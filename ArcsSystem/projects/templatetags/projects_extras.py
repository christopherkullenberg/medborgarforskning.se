

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


def get_keywords_trans(model_thing, lang):
	return model_thing.get_keywords(lang)




register.filter("get_keywords", get_keywords)
register.filter("get_keywords_trans", get_keywords_trans)