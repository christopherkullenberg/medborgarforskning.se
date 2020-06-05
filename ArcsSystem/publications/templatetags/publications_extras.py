import datetime
from django import template
from publications.views import SearchPublicationsView


register = template.Library()



def query_publications(query):
    result = SearchPublicationsView.get_queryset_template(query)
    return result

def list_5_recent_publications(query):
    result = SearchPublicationsView.list_5_recent_publications(query)
    return result


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)
register.filter('query_publications', query_publications)
register.filter('list_5_recent_publications', list_5_recent_publications)
