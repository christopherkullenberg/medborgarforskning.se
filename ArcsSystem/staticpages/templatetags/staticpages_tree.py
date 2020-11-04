import datetime
from django import template
from staticpages.models import Page
from staticpages.views import StaticPages
from staticpages.views import SearchView

register = template.Library()

def get_page(slug):
    page = StaticPages.get_page(slug)
    return page

def get_menu(category):
    menu = StaticPages.get_menu(category)
    return menu

register.filter('get_page', get_page)
register.filter('get_menu', get_menu)
