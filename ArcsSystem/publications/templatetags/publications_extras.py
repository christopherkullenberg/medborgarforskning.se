import datetime
from django import template
from publications.views import SearchPublicationsView
from django.db.models import Q
from collections import defaultdict
from projects.models import KeywordEng

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


#
def defaultdict_nodes():
	return {"value": 0, "group": 2}

#
def defaultdict_links():
	return {"value": 0}

#
def defaultdict_links_super():
	return defaultdict(defaultdict_links)

def get_bigest_links(di, alowed_links_per_node = 3):

	anwer = [""] * alowed_links_per_node
	biggest_links = [0] * alowed_links_per_node

	for k,v in di.items():
		for index in range(alowed_links_per_node):
			if v["value"] > biggest_links[index]:
				biggest_links[index] = v["value"]
				anwer[index] = k
				break
	re = []
	for index in range(alowed_links_per_node):
		if anwer[index] != "":
			re.append([anwer[index], {"value": biggest_links[index]}] )   

	return re





#
def convert_dict(json_di, value=1):

	r_di = {"nodes" : [ {"id": k, "group": v["group"] , "value": v["value"]} for k, v in json_di["nodes"].items() if v["value"] > value ]}
	r_di["links"] = []

	for k, v in json_di["links"].items():

		for k2, v2 in get_bigest_links(v,  1):  #get_bigest_links(v, int(json_di["nodes"][k]["value"]//10 ) + 2): #v.items():


			if v2["value"] > value :

				r_di["links"].append({"source": k, "target": k2, "value": v2["value"]})

	return json.dumps(r_di)



	#with open("media/miserables.json", "w") as f:

		#json.dump(r_di, f)



# this gets all the related things
# this is messy, and can be divide in to sub functions
def get_all_related(Article, lang ="en", use="all"):

	#limit for pub, pro and theme. Can change to one for each one
	limit_things = 16

	# these are the tabs that are created
	dict_key_thing = ["Project", "Theme"]

	#allway exlude
	uni_exclude_keys = ["citizen science", "newtech"]

	# If true: include keywords from article
	test = True

	# di is where all the Q data is stored.
	# di, sorts pub, pro and theme after kw-simularaties with article.
	di = {}

	# this is
	json_di = {"nodes": defaultdict(defaultdict_nodes), "links": defaultdict(defaultdict_links_super)}

 	# init dict part
	di["pub"] = defaultdict(list)
	di["pub"]["not"] = defaultdict(list)

	for dict_key in dict_key_thing:
		di[dict_key] = defaultdict(list)
		di[dict_key]["not"] = defaultdict(list)
		di[dict_key]["sv"] = {}
		di[dict_key]["sv"]["not"] = defaultdict(list)

	# use it art.kw, this is for prio and use in get_custom_html
	use = Article.keywords.all().exclude(keyword__in=uni_exclude_keys)


	# every kw
	amount_pub = 0
	for kw in use:

		# checks all articles
		for art in kw.Article.all().exclude(id__in=di["pub"]["not"][kw.id] + [Article.id]):
			amount_pub += 1
			result = art.keywords.all().exclude(keyword__in=uni_exclude_keys)
			#prio
			result_prio =[x for x in result if x in use]
			#sorts
			di["pub"][len(result_prio)].append([art, result, result_prio])
			# exclude art from other kw find art
			for x in result:
				di["pub"]["not"][x.id].append(art.id)
		#all lines
		for line in kw.line.all():
			#all thems
			for theme in line.Theme.all().exclude(id__in=di["Theme"]["not"][kw.id] ):
				result = [l for l in theme.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys) ]
				di["Theme"][len(result)].append([theme,[l.eng for l in result]])
				for l in result:
					di["Theme"]["not"][l.eng.id].append(theme.id)
					if l.swe != None:
						di["Theme"]["sv"]["not"][l.swe.id].append(theme.id)

			for project in line.Project.all().exclude(id__in=di["Project"]["not"][kw.id] ):
				result = [l for l in project.keyword_lines.filter(~Q(eng = None)).exclude(eng__keyword__in=uni_exclude_keys) ]
				di["Project"][len(result)].append([project, [l.eng for l in result]])
				for l in result:
					di["Project"]["not"][l.eng.id].append(project.id)
					if l.swe != None:
						di["Project"]["sv"]["not"][l.swe.id].append(project.id)
			if line.swe != None:
				line_sv = line.swe.line.filter(eng=None).first()
				if line_sv != None:
					for theme2 in line_sv.Theme.all().exclude(id__in=di["Theme"]["sv"]["not"][line_sv.swe.id]):
						result = [l.swe for l in theme2.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys)]
						di["Theme"][len(result)].append([theme2, result])
						for x in result:
							di["Theme"]["sv"]["not"][x.id].append(theme2.id)
					for project2 in line_sv.Project.all().exclude(id__in=di["Project"]["sv"]["not"][line_sv.swe.id] ):
						result = [l.swe for l in project2.keyword_lines.filter(~Q(swe = None)).exclude(eng__keyword__in=uni_exclude_keys) ]
						di["Project"][len(result)].append([project2, result])
						for x in result:
							di["Project"]["sv"]["not"][x.id].append(project2.id)

	nav_html = ' <ul class="nav nav-tabs"> '
	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '
	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "" + '" data-toggle="tab" href="#'+"pub"+'">'+"Publications"+ str(amount_pub)+'</a> </li> '
	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "" +'">  <div class="row" > '
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

			div_html += art[0].get_custom_html(lang, [x2.id for x2 in art[2]] ) #art[1])
			count += 1

	div_html += ' </div></div>'
	for grup_num, thing in enumerate(dict_key_thing):
		nav_html += ' <li class="nav-item"> <a class="nav-link ' + thing + '" data-toggle="tab" href="#'+thing+'">'+thing+'</a> </li> '
		div_html += ' <div id="'+thing+'" class="tab-pane container '+ thing +'">  <div class="row" > '
		count = 0
		for x in range(60, -1, -1):
			if count == limit_things:
				break

			for art in di[thing].get(x, []):
				if count == limit_things:
					break

				for c, kw in enumerate(art[1],1):
					if count == limit_things:
						break

					json_di["nodes"][kw.keyword]["value"] += 1
					json_di["nodes"][kw.keyword]["group"] = grup_num
					for kw2 in art[1][c:]:
						json_di["links"][kw.keyword][kw2.keyword]["value"] += 1

				div_html += art[0].get_custom_html(lang, [x2.id for x2 in use] ) #art[1])
				count += 1

		div_html += ' </div></div>'

	nav_html += ' <li class="nav-item"> <a class="nav-link active" data-toggle="tab" href="#svg_map_pub"> Keyword map </a> </li> '
	div_html += ''' <div id="svg_map_pub" class="tab-pane active" style="background: black" >  <svg id="rel_graph" style="width:100%;height:1000px;"  width="1000" height="1000">
	'''  + '''

	 <text x="300" y="70"style="fill:red;font-size:25px;"> Themes </text>  <text x="500" y="70" style="fill:green;font-size:25px;"> Projects </text>  <text x="700" y="70" style="fill:blue;font-size:25px;"> Publications </text>

	 <rect x="40" y="40" width="190" height="300" style="stroke:white;stroke-width:1;" />

	 <text id="info_text_svg" x="50" y="80" style="fill:white;font-size:15px;">

	 	<tspan x="50"> Name: </tspan>
	    <tspan x="50" dy="20" id="name" ></tspan>
	    <tspan x="50" dy="40"> Number of occurrences: </tspan>
    	<tspan id="value" x="50"  dy="20"  > </tspan>
    	<tspan style="fill:blue;font-size:15px;" x="50"  dy="40"  > <a id="link" href="#">Go to keyword</a>  </tspan>
	 </text>
	'''  +  '''</svg> </div> '''

	if test:
		for c, kw in enumerate(use,1):
			json_di["nodes"][kw.keyword]["value"] += 1
			for kw2 in use[c:]:
				json_di["links"][kw.keyword][kw2.keyword]["value"] += 1
	nav_html += ' </ul> '
	div_html += ' </div> </div> <br> <br> <br> <br>'


	#convert_dict(json_di)

	return [[nav_html + div_html, convert_dict(json_di)]]


def test_sort(art):

	return art.id




# def get_related_all(Article, lang ="en", use="all"):

# 	limit_things = 8


# 	di = {}

# 	json_di = {"nodes": defaultdict(defaultdict_nodes), "links": defaultdict(defaultdict_links_super)}



# 	di["pub"] = defaultdict(list)

# 	di["pub"]["max"] = 0


# 	di["pub"]["not"] = defaultdict(list)




# 	use = Article.keywords.all().exclude(keyword__in=["citizen science", "newtech"])

# 	for kw in use:


# 		for art in kw.Article.all().exclude(id__in=di["pub"]["not"][kw.id] + [Article.id]):




# 			result = [x for x in art.keywords.all().exclude(keyword__in=["citizen science", "newtech", kw.keyword]) if x in use]


# 			di["pub"][len(result)].append([art, result + [kw]])

# 			for x in result:

# 				di["pub"]["not"][x.id].append(art.id)

# 	nav_html = ' <ul class="nav nav-tabs"> '

# 	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '


# 	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "pub" + '" data-toggle="tab" href="#'+"pub"+'">'+"pub"+'</a> </li> '
# 	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "pub" +'">  <div class="row" > '
# 	count = 0
# 	for x in range(60, -1, -1):

# 		if count == limit_things:
# 			break

# 		for art in di["pub"].get(x, []):

# 			if count == limit_things:
# 				break

# 			for c, kw in enumerate(art[1]):

# 				if count == limit_things:
# 					break

# 				json_di["nodes"][kw.keyword]["value"] += 1


# 				for kw2 in art[1][c+1:]:

# 					json_di["links"][kw.keyword][kw2.keyword]["value"] += 1








# 			div_html += art[0].get_custom_html(lang, [x.id for x in art[1]]) #art[1])

# 			count += 1





# 		div_html += ' </div></div>'



# 	nav_html += ' </ul> '
# 	div_html += ' </div> </div> <br> <br> <br> <br>'




# 	return nav_html + div_html
















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



def get_keyword_en_from_name(name):

	try:
		return KeywordEng.objects.get(kewword=name).id
	except Exception as e:
		return ""





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
#register.filter("get_related_all", get_related_all)

register.filter("get_all_related", get_all_related)
