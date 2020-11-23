from django.db.models import Q
from collections import defaultdict
from projects.models import KeywordEng
from django import template


import json


# import db_classes

from projects.models import ProjectEntry
from workpackages.models import Theme
from publications.models import Article


register = template.Library()





#
def defaultdict_nodes():
	return {"value": 0, "group": 2}

#
def defaultdict_links():
	return {"value": 0}

#
def defaultdict_links_super():
	return defaultdict(defaultdict_links)

#

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

def convert_dict(json_di, value=1):

	r_di = {"nodes" : [ {"id": k, "group": v["group"] , "value": v["value"]} for k, v in json_di["nodes"].items() if v["value"] > value ]}
	r_di["links"] = []

	for k, v in json_di["links"].items():

		for k2, v2 in get_bigest_links(v,  1):  #get_bigest_links(v, int(json_di["nodes"][k]["value"]//10 ) + 2): #v.items():


			if v2["value"] > value :

				r_di["links"].append({"source": k, "target": k2, "value": v2["value"]})

	return json.dumps(r_di)


# get theme, projects,
# def get_related_db_class(db_class, di, exclude=[]):
# 	pass


# def get_all_related(this_db_class, lang ="en", use="all"):


# 	#limit for pub, pro and theme. Can change to one for each one
# 	limit_things = 16

# 	# these are the tabs that are created
# 	dict_key_thing = ["Project", "Theme"]

# 	# find these
# 	#db_classes = {"Project":ProjectEntry,"Theme" :Theme,"publication":, Article}
# 	db_classes = {"Project":[],"Theme" :[],"publication":[]}

# 	#allway exlude
# 	uni_exclude_keys = ["citizen science", "newtech"]


# 	# If true: include keywords from article
# 	test = True

# 	# di is where all the Q data is stored.
# 	# di, sorts pub, pro and theme after kw-simularaties with article.
# 	di = {}

# 	# this is
# 	json_di = {"nodes": defaultdict(defaultdict_nodes), "links": defaultdict(defaultdict_links_super)}

#  	# init dict part
# 	di["pub"] = defaultdict(list)
# 	di["pub"]["not"] = defaultdict(list)

# 	for dict_key in dict_key_thing:
# 		di[dict_key] = defaultdict(list)
# 		di[dict_key]["not"] = defaultdict(list)
# 		di[dict_key]["sv"] = {}
# 		di[dict_key]["sv"]["not"] = defaultdict(list)

# 	# use it art.kw, this is for prio and use in get_custom_html

# 	if type(this_db_class) == KeywordEng:
# 		use = [KeywordEng]
# 		if this_db_class.keyword in uni_exclude_keys:
# 			uni_exclude_keys.remove(this_db_class.keyword)


# 	elif type(this_db_class) == Article:
# 		use = this_db_class.keywords.all().exclude(keyword__in=uni_exclude_keys)

# 	else:
# 		use = [line.eng for line in this_db_class.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys, eng=None)]

# 		if type(this_db_class) == Theme:
# 			db_classes["Theme"].append(this_db_class.id)

# 		if type(this_db_class) == ProjectEntry:
# 			db_classes["Project"].append(this_db_class.id)




# 	# every kw
# 	amount_pub = 0






	# for db_class in db_classes:

	# 	if type(this_db_class) == db_class:
	# 		get_related_db_class(db_class, di, [this_db_class.id] )
	# 	else:
	# 		get_related_db_class(db_class, di, [])






def get_all_related(this_db_class, lang ="en", use="all"):




	#limit for pub, pro and theme. Can change to one for each one
	limit_things = 16

	# these are the tabs that are created
	dict_key_thing = ["Project", "Theme"]

	# find these
	#db_classes = {"Project":ProjectEntry,"Theme" :Theme,"publication":, this_db_class}
	db_classes = {"project":[],"theme" :[],"publication":[]}

	#allway exlude
	uni_exclude_keys = ["citizen science", "newtech"]


	# If true: include keywords from this_db_class
	test = True

	# di is where all the Q data is stored.
	# di, sorts pub, pro and theme after kw-simularaties with this_db_class.
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

	if type(this_db_class) == KeywordEng:
		use = [this_db_class]

		if this_db_class.keyword in uni_exclude_keys:
			uni_exclude_keys.remove(this_db_class.keyword)


	elif type(this_db_class) == Article:
		use = this_db_class.keywords.all().exclude(keyword__in=uni_exclude_keys)
		db_classes["publication"].append(this_db_class.id)

	else:
		use = [line.eng for line in this_db_class.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys).exclude(eng__isnull=True)]
		if type(this_db_class) == Theme:
			db_classes["theme"].append(this_db_class.id)

		elif type(this_db_class) == ProjectEntry:
			db_classes["project"].append(this_db_class.id)


	if len(use) == 0:
		return["", {}]


	# every kw
	amount_pub = 0
	amount_pro = 0
	amount_the = 0

	if len(use) == 1:
		q_set = limit_things
	else:
		q_set = None

	for kw in use:

		# checks all this_db_classs
		for art in kw.Article.all().exclude(id__in=di["pub"]["not"][kw.id] + db_classes["publication"])[:q_set]:
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
			for theme in line.Theme.all().exclude(id__in=di["Theme"]["not"][kw.id] + db_classes["theme"])[:q_set]:
				amount_the += 1
				result = theme.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys).exclude(eng__isnull=True)
				result_prio =[x for x in result if x in use]
				di["Theme"][len(result_prio)].append([theme,[l.eng for l in result]])
				for l in result:
					di["Theme"]["not"][l.eng.id].append(theme.id)

			for project in line.Project.all().exclude(id__in=di["Project"]["not"][kw.id] + db_classes["project"])[:q_set]:
				amount_pro += 1
				result = project.keyword_lines.all().exclude(eng__keyword__in=uni_exclude_keys).exclude(eng__isnull=True)
				result_prio =[x for x in result if x in use]
				di["Project"][len(result_prio)].append([project, [l.eng for l in result]])
				for l in result:
					di["Project"]["not"][l.eng.id].append(project.id)



	if len(use) == 1:
		if type(this_db_class) == KeywordEng:

			amount_pub = this_db_class.Article.all().count()

		# add for others


	nav_html = ' <ul class="nav nav-tabs"> '
	div_html = ' <div class="col-12">  <div class="tab-content"> <br> '
	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "" + '" data-toggle="tab" href="#'+"pub"+'">'+"Publications ("+ str(amount_pub)+')</a> </li> '
	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "" +'">  <div class="row" > '
	count = 0




	for x in range(30, -1, -1): # this is bad can do di.keys.sort()
		if count == limit_things:
			break

		for art in di["pub"].get(x, []):
			if count == limit_things:
				break

			for c, kw in enumerate(art[1],1):

				json_di["nodes"][kw.keyword]["value"] += 1
				for kw2 in art[1][c:]:
					json_di["links"][kw.keyword][kw2.keyword]["value"] += 1

			div_html += art[0].get_custom_html(lang, [x2.id for x2 in art[2]] ) #art[1])
			count += 1

	count_list = [amount_pro, amount_the]


	div_html += ' </div></div>'

	for grup_num, thing in enumerate(dict_key_thing):
		nav_html += ' <li class="nav-item"> <a class="nav-link ' + thing + '" data-toggle="tab" href="#'+thing+'">'+thing+' (' + str(count_list[grup_num])+ ')</a> </li> '
		div_html += ' <div id="'+thing+'" class="tab-pane container '+ thing +'">  <div class="row" > '
		count = 0
		for x in range(60, -1, -1):
			if count == limit_things:
				break

			for art in di[thing].get(x, []):

				if count == limit_things:
					break

				for c, kw in enumerate(art[1],1):


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


	return [[nav_html + div_html, convert_dict(json_di, 1 )]]


def get_keyword(line, lang):

	return line.get_custom_html(lang)

register.filter("get_keyword", get_keyword)
register.filter("get_all_related", get_all_related)
