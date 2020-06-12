import datetime
from django import template
from publications.views import SearchPublicationsView


register = template.Library()



# def query_publications(query):
#     result = SearchPublicationsView.get_queryset_template(query)
#     return result

def query_publications(query, number=5):
    # TODO - this now only returns 5 pubs, abstract this in the future.
    result = SearchPublicationsView.related_publications(query, number)
    return result

def recent_publications(number=3):
    result = SearchPublicationsView.recent_publications(number)
    return result



def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)
register.filter('query_publications', query_publications)
register.filter('recent_publications', recent_publications)
