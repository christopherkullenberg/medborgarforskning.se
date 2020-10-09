import datetime
from django import template
from staticpages.models import Page
from staticpages.views import Page

register = template.Library()

def get_page(slug):
    result = Page.get_absolute_url(slug)
    return result

register.filter('get_page', get_page)
