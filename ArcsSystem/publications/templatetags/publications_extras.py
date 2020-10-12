import datetime
from django import template
from publications.views import SearchPublicationsView


register = template.Library()


# this function will place br in string att length
# -------------------------- <br>
# -------------------------- <br>
# -------------------------- <br>
# And it will not divide words
def break_text(string, length):

	string = string.title
	str_len = len(string)
	if str_len <= length:
		return string

	li = string.split(" ")
	new_string = li[0]
	count = len(li[0])
	for segment in li[1:]:
		if count + len(segment) >= length:
			new_string += "<br>" + segment
			count = len(segment)
		else:
			new_string += " " + segment
			count += len(segment)+1

	return new_string

def break_slug(string):
	return string.replace("_", " ")
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
register.filter('break_text', break_text)
register.filter('break_slug', break_slug)
