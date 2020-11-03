

from django import template
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe, ScienceType, STATUS_CHOICES


register = template.Library()




def get_keywords(string):

    if string == "swe":

        return [k.keyword for k in KeywordSwe.objects.all()]

    if string == "eng":

        return [k.keyword for k in KeywordEng.objects.all()]

    return []


def get_keywords_trans(model_thing, lang):
	return model_thing.get_keywords(lang)



def get_all_status(limit=20):
    return [x[1] for x in STATUS_CHOICES]

def get_science_types(limit=20):
    return ScienceType.objects.all()[:limit]
register.filter("get_all_status", get_all_status)
register.filter("get_keywords", get_keywords)
register.filter("get_keywords_trans", get_keywords_trans)
register.filter("get_science_types", get_science_types)
