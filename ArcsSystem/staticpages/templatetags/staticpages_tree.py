import datetime
from django import template
from staticpages.views import TreeView
from staticpages.views import CategoryView


register = template.Library()



def get_categories(query):
    result = TreeView.get_categories()
    return result

def get_category(query):
    result = CategoryView.get_category(query)
    return result





register.filter('get_categories', get_categories)
register.filter('get_category', get_category)
