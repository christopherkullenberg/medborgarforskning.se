import datetime
from django import template
from blog.views import SearchBlogView


register = template.Library()



def latest_blogs(query):
    result = SearchBlogView.get_queryset_template(query)
    return result


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)
register.filter('latest_blogs', latest_blogs)
