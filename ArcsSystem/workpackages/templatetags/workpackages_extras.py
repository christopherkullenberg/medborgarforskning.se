import datetime
from django import template
from workpackages.models import WorkPackage, Theme
from publications.models import Article


register = template.Library()


def break_slug(string):
    return string.replace("_", " ")
def get_wp_name(WPname):
    result = WorkPackage.objects.get(name=WPname)
    return result.name
    '''
    if language == "en":
        return result.name_en
    elif language == "sv":
        return result.name_sv
    '''

def get_rel_pubs(theme):

    use = [line.eng.id for line in theme.keyword_lines.all() if line.eng]
    return [Article.objects.get(id= int(art_id)).get_custom_html(use=use) for art_id in theme.get_pub_ids()]



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

register.filter('get_rel_pubs', get_rel_pubs)
register.filter('get_wp_name', get_wp_name)
register.filter('get_wp_intro', get_wp_intro)
register.filter('get_wp_detailed_content', get_wp_detailed_content)
register.filter('get_wp_themes', get_wp_themes)
register.filter("break_slug", break_slug)
