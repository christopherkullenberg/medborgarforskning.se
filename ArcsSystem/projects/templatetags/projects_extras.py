from django import template
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe, ScienceType, STATUS_CHOICES, KeywordLine, DATABASE_CHOICES


register = template.Library()




def get_keywords(string):

	if string == "swe":

		return [k.keyword for k in KeywordSwe.objects.all()]

	if string == "eng":

		return [k.keyword for k in KeywordEng.objects.all()]

	return []


def get_keywords_objects(string):


	if string == "swe":

		return KeywordSwe.objects.all()

	if string == "eng":

		return KeywordEng.objects.all()
	return []



def get_keywords_trans(model_thing, lang):
	return model_thing.get_keywords(lang)

def get_all_status(limit=20):
	return STATUS_CHOICES

def get_science_types(limit=20):
	return ScienceType.objects.all()[:limit]

def get_origin_database(limit=20):
	return DATABASE_CHOICES

def line_is_project(not_use):

	return [KeywordLine.objects.exclude(Project=None)]




register.filter("line_is_project", line_is_project)
register.filter("get_keywords_objects", get_keywords_objects)
register.filter("get_all_status", get_all_status)
register.filter("get_keywords", get_keywords)
register.filter("get_keywords_trans", get_keywords_trans)
register.filter("get_science_types", get_science_types)
register.filter("get_origin_database", get_origin_database)
