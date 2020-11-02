from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from projects.models import KeywordEng

from organizations.models import Organization
from django.db.models import Q

from projects.models import KeywordEng, KeywordSwe, KeywordLine

'''
# Quick Fuction based template
def template_view(request):
'''
'''
    context = {
        }
    return render(request, 'exampletemplate.html', context)
'''


class KeywordList(ListView):
    model = KeywordEng
    template_name = 'keywords/keyword_list.html'
    queryset = KeywordEng.objects.filter(keyword="end 49\\2002")


def keywordDetailView(request, name):

	if request.method == "GET":

		template_name = 'keywords/keyword_detail.html'

		context = {"object": get_object_or_404(KeywordEng, keyword=name)}

		# line = context["object"].line.get(swe = None)

		# context["themes"] = line.Theme.all()
		# context["themes_amount"] = context["themes"].count()

		# context["projects"] = line.Project.all()
		# context["projects_amount"] = context["projects"].count()

		# context["blog"] = line.Theme.all()
		# context["themes_amount"] = context["themes"].count()


		return render(request, template_name, context)





	raise 404




class KeywordDetailView(DetailView):

    model = KeywordEng
    template_name = 'keywords/keyword_detail.html'



def keywords_to_context(obj, context):

    context["keyword_line"] = []
    c = 0
    for c, line in enumerate(obj.keyword_lines.all(),1):
        context["keyword_line"].append(line.get_line)
    context["keyword_len"] = c



# make kw and kwl and update obj
def update_object_KWL(obj, request,  stop):


    obj.keyword_lines.clear()


    sve_string = []
    eng_string = []

    for nr in range(1, stop):
        if "Keyword_sve_" + str(nr) in request.POST or "Keyword_eng_" + str(nr) in request.POST:


            if "Keyword_sve_" + str(nr) in request.POST:
                sve_string.append(request.POST["Keyword_sve_" + str(nr)].replace("&", ""))
            else:
                sve_string.append("")


            if "Keyword_eng_" + str(nr) in request.POST:
                eng_string.append(request.POST["Keyword_eng_" + str(nr)].replace("&", ""))
            else:
                eng_string.append("")


    for key_sv, key_en in zip(sve_string, eng_string):


        # if both are empty continue
        if key_sv == "" and key_en == "":
            continue

        # if sv is empty but not en
        if key_sv == "":

            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()
            options = model_keyword_eng.line.filter(swe=None)

            if len(options) > 0:

                obj.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(eng=model_keyword_eng)
                model_keyword_line.save()

                obj.keyword_lines.add(options.first())


        # if sv is empty but not en
        elif key_en == "":

            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()
            options = model_keyword_swe.line.filter(eng=None)

            if len(options) > 0:

                obj.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe)
                model_keyword_line.save()

                obj.keyword_lines.add(options.first())

        # both are filed-in
        else:

            # en key
            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()


            # sv key
            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()


            options = model_keyword_swe.line.filter(eng=model_keyword_eng)

            if len(options) > 0:

                obj.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe, eng=model_keyword_eng)
                model_keyword_line.save()

                obj.keyword_lines.add(options.first())

    obj.save()
