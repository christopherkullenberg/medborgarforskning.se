import datetime
from django import template
from publications.views import SearchPublicationsView
from django.db.models import Q
from collections import defaultdict

import json

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

# def get_related_all_2(Article):
# 	li = []
# 	keyword = Article.keywords.all()
# 	for th in keyword:
# 		if len(th.Theme.all()) > 0:

# 			li += th.Theme.all()


# 	return li

# def get_related_all(Article):



# 	themes = []
# 	projects = []
# 	blogs = []

# 	publications = []

# 	theme_count = 0
# 	theme_count_limit = 20

# 	projects_count = 0
# 	projects_count_limit = 20

# 	blogs_count = 0
# 	blogs_count_limit = 20

# 	publications = []
# 	publications_count = 0
# 	publications_count_limit = 40



# 	for kw in Article.keywords.all():



# 		for art in kw.Article.all():
# 			if art != Article and art not in publications:
# 				publications.append(art)
# 				publications_count += 1
# 				if publications_count == publications_count_limit:
# 					break


# 		for line in kw.line.all():

# 			for th in line.Theme.all():
# 				if th not in themes:
# 					themes += [th]
# 					theme_count += 1
# 					if theme_count == theme_count_limit:
# 						break

# 			for pr in line.Project.all():
# 				if pr not in projects:
# 					projects += [pr]
# 					projects_count += 1
# 					if projects_count == projects_count_limit:
# 						break

# 			for bl in line.Blog.all():
# 				if bl not in blogs:
# 					blogs += [bl]
# 					blogs_count += 1
# 					if blogs_count == blogs_count_limit:
# 						break



# 			if line.swe:
# 				for line in line.swe.line.filter(eng=None):

# 					for line in kw.line.all():

# 						for th in line.Theme.all():
# 							if theme_count == theme_count_limit:
# 								break
# 							if th not in themes:
# 								themes += [th]

# 						for pr in line.Project.all():
# 							if projects_count == projects_count_limit:
# 								break
# 							if pr not in projects:
# 								projects += [pr]

# 						for bl in line.Blog.all():
# 							if blogs_count == blogs_count_limit:
# 								break
# 							if bl not in blogs:
# 								blogs += [bl]


# 	return [themes, projects, blogs, publications]


def defaultdict_nodes():
	return {"value": 0, "group": []}

def defaultdict_links():
	return {"value": 0}

def defaultdict_links_super():
	return defaultdict(defaultdict_links)

def convert_dict(json_di):

	r_di = {"nodes" : [ {"id": k, "group": 1, "value": v["value"]} for k, v in json_di["nodes"].items() ]}
	r_di["links"] = []

	for k, v in json_di["links"].items():

		for k2, v2 in v.items():

			r_di["links"].append({"source": k, "target": k2, "value": v2["value"]})

	with open("C:/django-pro/medborgarforskning.se/ArcsSystem/media/miserables.json", "w") as f:

		json.dump(r_di, f)





def get_all_related(Article, lang ="en", use="all"):

	limit_things = 20

	# ha med art
	test = True


	di = {}

	json_di = {"nodes": defaultdict(defaultdict_nodes), "links": defaultdict(defaultdict_links_super)}



	di["pub"] = defaultdict(list)

	di["pub"]["max"] = 0


	di["pub"]["not"] = defaultdict(list)




	use = Article.keywords.all().exclude(keyword__in=["citizen science", "newtech"])

	for kw in use:




		for art in kw.Article.all().exclude(id__in=di["pub"]["not"][kw.id] + [Article.id]):



			
			result = [x for x in art.keywords.all().exclude(keyword__in=["citizen science", "newtech", kw.keyword]) if x in use]

	
			di["pub"][len(result)].append([art, result + [kw]])

			for x in result:

				di["pub"]["not"][x.id].append(art.id)





	nav_html = ' <ul class="nav nav-tabs"> ' 

	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '


	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "pub" + '" data-toggle="tab" href="#'+"pub"+'">'+"pub"+'</a> </li> '
	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "pub" +'">  <div class="row" > '
	count = 0
	for x in range(60, -1, -1):


		if count == limit_things:
			break

		for art in di["pub"].get(x, []):


			if count == limit_things:
				break

			for c, kw in enumerate(art[1],1):

				if count == limit_things:
					break

				json_di["nodes"][kw.keyword]["value"] += 1


				for kw2 in art[1][c:]:

					json_di["links"][kw.keyword][kw2.keyword]["value"] += 1








			#div_html += art[0].get_custom_html(lang, [x2.id for x2 in art[1]] ) #art[1])

			count += 1



		

		div_html += ' </div></div>'

		


		if test:


			for c, kw in enumerate(use,1):

				json_di["nodes"][kw.keyword]["value"] += 1


				for kw2 in use[c:]:

					json_di["links"][kw.keyword][kw2.keyword]["value"] += 1



	nav_html += ' </ul> '
	div_html += ' </div> </div> <br> <br> <br> <br>'

	convert_dict(json_di)

	return json_di

			
	return nav_html + div_html




def get_related_all(Article, lang ="en", use="all"):

	limit_things = 8


	di = {}

	json_di = {"nodes": defaultdict(defaultdict_nodes), "links": defaultdict(defaultdict_links_super)}



	di["pub"] = defaultdict(list)

	di["pub"]["max"] = 0


	di["pub"]["not"] = defaultdict(list)




	use = Article.keywords.all().exclude(keyword__in=["citizen science", "newtech"])

	for kw in use:


		for art in kw.Article.all().exclude(id__in=di["pub"]["not"][kw.id] + [Article.id]):



			
			result = [x for x in art.keywords.all().exclude(keyword__in=["citizen science", "newtech", kw.keyword]) if x in use]

	
			di["pub"][len(result)].append([art, result + [kw]])

			for x in result:

				di["pub"]["not"][x.id].append(art.id)

	nav_html = ' <ul class="nav nav-tabs"> ' 

	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '


	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "pub" + '" data-toggle="tab" href="#'+"pub"+'">'+"pub"+'</a> </li> '
	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "pub" +'">  <div class="row" > '
	count = 0
	for x in range(60, -1, -1):

		if count == limit_things:
			break

		for art in di["pub"].get(x, []):

			if count == limit_things:
				break

			for c, kw in enumerate(art[1]):

				if count == limit_things:
					break

				json_di["nodes"][kw.keyword]["value"] += 1
				json_di["nodes"][kw.keyword]["group"].append(art[0].id)

				for kw2 in art[1][c+1:]:

					json_di["links"][kw.keyword][kw2.keyword]["value"] += 1








			div_html += art[0].get_custom_html(lang, [x.id for x in art[1]]) #art[1])

			count += 1



		

		div_html += ' </div></div>'



	nav_html += ' </ul> '
	div_html += ' </div> </div> <br> <br> <br> <br>'



			
	return nav_html + div_html
















# def get_related_all(Article, lang ="en", use="all"):

# 	#active = "publications"

# 	use = Article.keywords.all()
# 	use = Article.keywords.filter((~Q(keyword = "citizen science"))).exclude(keyword__in=["citizen science", "newtech"])

# 	class_edit_dict = {
# 		"themes": "",
# 		"projects": "",
# 		"blogs": "",
# 		"publications": "active",

# 	}



# 	return_dict = {
# 		"themes":[],
# 		"projects": [],
# 		"blogs": [],
# 		"publications": [],
# 	}

	




# 	things_limit = 20 

# 	themes = []
# 	projects = []
# 	blogs = []

# 	publications = []

# 	theme_count = 0
# 	theme_count_limit = things_limit

# 	projects_count = 0
# 	projects_count_limit = things_limit

# 	blogs_count = 0
# 	blogs_count_limit = things_limit

# 	publications = []
# 	publications_count = 0
# 	publications_count_limit = things_limit



# 	for kw in use:


# 		if publications_count < publications_count_limit:

# 			for art in kw.Article.all():
# 				if art != Article and art not in return_dict["publications"]:
# 					return_dict["publications"].append(art)
# 					publications_count += 1
# 					if publications_count == publications_count_limit:
# 						break

# 		if theme_count < theme_count_limit:
# 			for line in kw.line.all():

# 				for th in line.Theme.all():
# 					if th not in return_dict["themes"]:
# 						return_dict["themes"] += [th]
# 						theme_count += 1
# 						if theme_count == theme_count_limit:
# 							break
# 		if projects_count < projects_count_limit:
# 			for pr in line.Project.all():
# 				if pr not in return_dict["projects"]:
# 					return_dict["projects"] += [pr]
# 					projects_count += 1
# 					if projects_count == projects_count_limit:
# 						break

# 		if blogs_count < blogs_count_limit:
# 			for bl in line.Blog.all():
# 				if bl not in return_dict["blogs"]:
# 					return_dict["blogs"] += [bl]
# 					blogs_count += 1
# 					if blogs_count == blogs_count_limit:
# 						break



# 			if line.swe != None:
# 				for line in line.swe.line.filter(eng=None):

# 					if theme_count < theme_count_limit:
# 						for th in line.Theme.all():
# 							if theme_count == theme_count_limit:
# 								break
# 							if th not in return_dict["themes"]:
# 								return_dict["themes"] += [th]


# 					if projects_count < projects_count_limit:
# 						for pr in line.Project.all():
# 							if projects_count == projects_count_limit:
# 								break
# 							if pr not in return_dict["projects"]:
# 								return_dict["projects"] += [pr]

# 					if blogs_count < blogs_count_limit:
# 						for bl in line.Blog.all():
# 							if blogs_count == blogs_count_limit:
# 								break
# 							if bl not in return_dict["blogs"]:
# 								return_dict["blogs"] += [bl]


# 	nav_html = ' <ul class="nav nav-tabs"> ' 

# 	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '

# 	for key, list_of_things in return_dict.items():

	
# 		nav_html += ' <li class="nav-item"> <a class="nav-link ' + class_edit_dict[key] + '" data-toggle="tab" href="#'+key+'">'+key+'</a> </li> '

# 		div_html += ' <div id="'+key+'" class="tab-pane container '+ class_edit_dict[key] +'">  <div class="row" > '

# 		for thing in list_of_things:

# 			div_html += thing.get_custom_html(lang, use)

# 		div_html += ' </div></div>'



# 	nav_html += ' </ul> '
# 	div_html += ' </div> </div> <br> <br> <br> <br>'

			
# 	return nav_html + div_html
# 	return [themes, projects, blogs, publications]


def items(iterable):
	return iterable.items()


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)
register.filter('items', items)
register.filter('query_publications', query_publications)
register.filter('recent_publications', recent_publications)
register.filter('break_text', break_text)
register.filter('break_slug', break_slug)
register.filter("get_related_all", get_related_all)

register.filter("get_all_related", get_all_related)



