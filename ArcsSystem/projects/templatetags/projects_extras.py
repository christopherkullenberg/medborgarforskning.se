from django import template
from django.template.defaultfilters import stringfilter
from workpackages.models import WorkPackage, Theme
from projects.models import KeywordEng, KeywordSwe, ScienceType, STATUS_CHOICES, KeywordLine, ProjectEntry
import os
import requests
import json
import re
import datetime
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

def euapi_projects(not_use):
    print("Getting EU projects")
    #return "hello"
    return api_get_projects()


@register.filter
@stringfilter
def get_recent_eu_projects(no_use):
    datedict = {}
    data = requests.get('https://eu-citizen.science/api/projects/')
    print("EUAPI Response code: " + str(data.status_code))
    jsondata = data.json()
    for project in jsondata:
        # 2020-12-18T17:22:29.027278Z'
        datedict[project['name']] = datetime.datetime.strptime(project['dateCreated'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #print(datedict)
    sortedlist = sorted(datedict, key=datedict.get) # orders by datetime of datecreated
    threemostrecentprojects = sortedlist[-3:]
    print(threemostrecentprojects)
    resultdict = {}
    for project in jsondata:
        if project['name'] in threemostrecentprojects:
            resultdict[project['name']] = [project['aim'],
                             project['keywords'],
                             project['topic'],
                             project['url'],
                             project['image1'],
                             project['country'],
                             project['dateCreated'],
                             project['start_date'],
                             project['end_date'],
                             project['latitude'],
                             project['longitude'],
                             project['status'],
                             project['mainOrganisation'],
                             project['id'],
                            ]

    wrapper = '''
                  <div class="row">
                <div id="main-page-slider" class="col">
                    <!--Carousel Wrapper-->
                    <div id="multi-item-example" class="carousel slide carousel-multi-item carousel-multi-item-selector" data-ride="carousel">
                        <div class="row slider-header d-flex justify-content-center align-items-center">
                            <div class="col">
                                <p class="font-weight-bold mb-0">Nya projekt!</p>
                            </div>
                            <div class="col">
                                <!--Controls-->
                                <div class="controls-top slider-top-controler ">
                                  <a class="btn-floating" href="#multi-item-example" data-slide="prev"><img id="icon-preview-rotate" class="next-icon-slider" src="/static/icons/Arrow_Right_Drop_Circle_Outline_Icon_3.png" alt="next-icon"/></a>
                                  <a class="btn-floating" href="#multi-item-example" data-slide="next"><img class="next-icon-slider" src="/static/icons/Arrow_Right_Drop_Circle_Outline_Icon_3.png" alt="next-icon"/></a>
                                </div>
                                <!--/.Controls-->
                            </div>
                        </div>

                      <!--Indicators-->
                      <ol class="carousel-indicators mb-0 ">
                        <li data-target="#multi-item-example" data-slide-to="0" class="active slider-selector"></li>
                        <li data-target="#multi-item-example" data-slide-to="1" class="slider-selector"></li>
                        <li data-target="#multi-item-example" data-slide-to="2" class="slider-selector"></li>
                      </ol>
                      <!--/.Indicators-->
                      <!--Slides-->
                      <div class="carousel-inner" role="listbox">

                     '''

    html = ""
    active = "active" # resets after first iteration below, only first shall be active
    for k, v in resultdict.items():
        #print(k)

        html += '''
        <div class="carousel-item ''' + active + ''' carousel-item-margin slider-color">

        <div class="col-md">
        <div class="card mb-2 border-slider-content">
        <a href="https://eu-citizen.science/project/''' + str(v[13]) + '''"><img class="d-block w-100" src="''' + remoteimage(v[4]) + '''" alt="''' + k + '''" /></a>
        <div class="card-body content-slider">
        <p class="font-weight-bold m-0">PROJEKT: ''' + k + ''' (''' + get_country_fullname(v[5]) + ''')</p>
        <!--<p class="font-weight-bold m-0">DESCRIPTION: Monitoring of fauna for insect activity."</p>
        <p class="font-weight-bold m-0"> "ONTACT POINT: Pavel Bina at SLU - [email or button]" </p>-->
        </div>
        </div>
        </div>
        </div>

        '''
        active = ""

    return(wrapper + html)



register.filter("line_is_project", line_is_project)
register.filter("get_keywords_objects", get_keywords_objects)
register.filter("get_all_status", get_all_status)
register.filter("get_keywords", get_keywords)
register.filter("get_keywords_trans", get_keywords_trans)
register.filter("get_science_types", get_science_types)
register.filter("euapi_projects", euapi_projects)
register.filter("get_recent_eu_projects", get_recent_eu_projects)
register.filter("countrylist", countrylist)
