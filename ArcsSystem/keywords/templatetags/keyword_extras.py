from django.db.models import Q
from collections import defaultdict
from projects.models import KeywordEng
from django import template


import json

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
def convert_dict(json_di, value):

	print(value)

	r_di = {"nodes" : [ {"id": k, "group": v["group"] , "value": v["value"]} for k, v in json_di["nodes"].items() if v["value"] > value ]}
	r_di["links"] = []

	for k, v in json_di["links"].items():

		for k2, v2 in v.items():


			if v2["value"] > value:

				r_di["links"].append({"source": k, "target": k2, "value": v2["value"]})




	with open("media/miserables.json", "w") as f:

		json.dump(r_di, f)



def get_all_related(Article, lang ="en", use="all"):

	#limit for pub, pro and theme. Can change to one for each one
	limit_things = 20000

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
	use = [Article]


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
	nav_html += ' <li class="nav-item"> <a class="nav-link ' + "active" + '" data-toggle="tab" href="#'+"pub"+'">'+"Publications"+ str(amount_pub)+'</a> </li> '
	div_html += ' <div id="'+"pub"+'" class="tab-pane container '+ "active" +'">  <div class="row" > '
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

				div_html += art[0].get_custom_html(lang, [x2.id for x2 in art[1]] ) #art[1])
				count += 1

		div_html += ' </div></div>'

	nav_html += ' <li class="nav-item"> <a class="nav-link " data-toggle="tab" href="#svg_map_pub"> Keyword map </a> </li> '
	div_html += ''' <div id="svg_map_pub" class="tab-pane " style="background: black" >  <svg id="rel_graph" style="width:100%;height:2000px;"  width="2000" height="2000">
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
	convert_dict(json_di, int(amount_pub/50))

	return nav_html + div_html

register.filter("get_all_related", get_all_related)
