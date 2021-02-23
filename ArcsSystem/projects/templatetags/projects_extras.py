from django import template
from django.template.defaultfilters import stringfilter
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe, ScienceType, STATUS_CHOICES, KeywordLine
import os
import requests
import json
import re
register = template.Library()



@register.filter
def countrylist(project):
	countrylist = []
	for c in project:
		if c['country'] not in countrylist:
			countrylist.append(c['country'])
		else:
			continue
	return sorted(countrylist)


@register.filter
def projectbycountry(project, listofcountries):
	print(listofcountries)
	if project['country'] in listofcountries:
		return project


@register.filter
def swedishprojects(project):
	if project['country'] in ["SE"]:
		return project

@register.filter
def scandinavianprojects(project):
	if project['country'] in ["SE", "DK", "NO", "FI", "IS"]:
		#print(project)
		return project

@register.filter
def allprojects(project):
	return project




@register.filter
@stringfilter
def localimage(value):
	filename = re.sub('https\:\/\/eu\-citizen.science\/media\/media\/images\/',
						'', value)
	localurl = '/media/EUimg/' + filename
	return localurl

@register.filter
@stringfilter
def remoteimage(value):
	remoteurl = re.sub('\/media\/media\/',
						'/media/', value)
	return remoteurl


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




def line_is_project(not_use):

	return [KeywordLine.objects.exclude(Project=None)]

def euapi_projects():
	return api_get_projects()


register.filter("line_is_project", line_is_project)
register.filter("get_keywords_objects", get_keywords_objects)
register.filter("get_all_status", get_all_status)
register.filter("get_keywords", get_keywords)
register.filter("get_keywords_trans", get_keywords_trans)
register.filter("get_science_types", get_science_types)
register.filter("euapi_projects", euapi_projects)
