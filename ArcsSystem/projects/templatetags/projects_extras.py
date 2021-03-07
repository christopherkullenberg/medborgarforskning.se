from django import template
from django.template.defaultfilters import stringfilter
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe, ScienceType, STATUS_CHOICES, KeywordLine, ProjectEntry
import os
import requests
import json
import re
from country_bounding_boxes import country_subunits_containing_point, country_subunits_by_iso_code


register = template.Library()

@register.filter
def get_country_fullname(string):
    countrylist = [c.name for c in country_subunits_by_iso_code(string)]
    print(countrylist)
    if len(countrylist) == 1:
        return countrylist[0]
    elif string == 'BE':
        return 'Belgium'
    elif string == 'ES':
        return 'Spain'
    elif string == 'PT':
        return 'Portugal'
    elif string == 'IT':
        return 'Italy'
    elif string == 'GB':
        return 'Great Britain'
    elif string == 'US':
        return 'USA'
    elif string == 'DK':
        return 'Denmark'
    elif string == 'FR':
        return 'France'
    elif string == 'NO':
        return 'Norway'
    else:

        return countrylist[-1]

@register.filter
def get_country_bbox(countryobject):
    try:
        boxes = [c.bbox for c in country_subunits_by_iso_code(countryobject.code)]
        if len(boxes) == 1:
            #print(boxes)
            #print(type(boxes))
            return boxes
        else:
            #print(boxes)
            #print(type(boxes))
            #print(boxes[0])
            return [boxes[0]]
    except IndexError:
        return None 




@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

@register.filter
def countrylist(name='countrylist'):
    countrylist = []
    for c in ProjectEntry.objects.all():
        if c.country not in countrylist:
            if len(c.country) > 1:
                print(c.country)
                countrylist.append(str(c.country))
    return(countrylist)





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
register.filter("countrylist", countrylist)
