import datetime
from django import template
from staticpages.views import TreeView
from staticpages.views import CategoryView
from staticpages.views import WhatsCitizenScience
from staticpages.views import SwedishCitizenScience
from staticpages.views import CaseStudies
from staticpages.views import FAQ
from staticpages.views import AditionalResources

register = template.Library()


def get_categories(query):
    result = TreeView.get_categories()
    return result

def get_category(query):
    result = CategoryView.get_category(query)
    return result

def get_citizen_science(number=1):
    result = WhatsCitizenScience.get_submenu(number)
    return result


def get_swedish_citizen_science(number=1):
    result = SwedishCitizenScience.get_submenu(number)
    return result

def get_case_studies(number=1):
    result = CaseStudies.get_submenu(number)
    return result

def get_faq(number=1):
    result = FAQ.get_submenu(number)
    return result

def get_additional_resources(number=1):
    result = AditionalResources.get_submenu(number)
    return result

register.filter('get_categories', get_categories)
register.filter('get_category', get_category)
register.filter('get_citizen_science', get_citizen_science)
register.filter('get_swedish_citizen_science', get_swedish_citizen_science)
register.filter('get_case_studies', get_case_studies)
register.filter('get_faq', get_faq)
register.filter('get_additional_resources', get_additional_resources)
