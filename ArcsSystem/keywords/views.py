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
