import datetime
from django import template
from staticpages.models import Page
from staticpages.views import StaticPages

register = template.Library()

def get_page(slug):
    page = StaticPages.get_page(slug)
    return page


register.filter('get_page', get_page)
