import datetime
from django import template
from workpackages.models import WorkPackage, Theme


register = template.Library()



def get_wp_name(WPname):
    result = WorkPackage.objects.get(name=WPname)
    return result.name

def get_wp_intro(WPname):
    result = WorkPackage.objects.get(name=WPname)
    return result.introduction

def get_wp_detailed_content(WPname):
    result = WorkPackage.objects.get(name=WPname)
    return result.detailed_content

def get_wp_themes(WPname):
    wp_pk = WorkPackage.objects.get(name=WPname)
    result = Theme.objects.filter(wp_parent=wp_pk.pk)
    return result



def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)
register.filter('get_wp_name', get_wp_name)
register.filter('get_wp_intro', get_wp_intro)
register.filter('get_wp_detailed_content', get_wp_detailed_content)
register.filter('get_wp_themes', get_wp_themes)
