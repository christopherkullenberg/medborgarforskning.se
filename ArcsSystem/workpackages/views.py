from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.generic import DetailView, ListView
from workpackages.models import WorkPackage, Theme
from django.views import View
from .models import Theme, WorkPackage
from publications.models import Article
from keywords.views import keywords_to_context, update_object_KWL
from projects.models import KeywordEng, KeywordSwe, KeywordLine
from django.http import JsonResponse
from django.http import Http404
# Create your views here.

# this is the view for the workpack home_page

def get_eng(string):

    return {
    "trans" : [line.eng.keyword for line in KeywordSwe.objects.get(keyword=string).line.all().exclude(eng=None)],
    "lang": "engelsk översättning"
    }


def get_swe(string):
    return {
    "trans" : [line.swe.keyword for line in KeywordEng.objects.get(keyword=string).line.all().exclude(swe=None)],
    "lang": "svensk översättning"
    }


def ajax_function(request):
    if request.is_ajax and request.method == "GET":
        kw_name = request.GET.get("kw", None)
        lang = request.GET.get("lang", None)
        if lang == "swe":
            trans_func = get_eng
        elif lang == "eng":
            trans_func = get_swe
        else:
            return JsonResponse({}, status = 400)
        return JsonResponse(trans_func(kw_name))
    return JsonResponse({}, status = 400)


class WorkpackagesListView(View):

    template_name = 'workpackages/workpackages_list.html'

    def get(self, request):

        context = {}
        superThemes = WorkPackage.objects.all()
        context["superThemes"] = superThemes
        context["list_theme"] = []
        for st in superThemes:
            context["list_theme"].append([st , Theme.objects.filter(wp_parent=st.id)])

        return render(request, self.template_name, context)

class WorkpackagesThemeView(View):
    template_name = 'workpackages/theme_view.html'

    def get(self, request, category):
        context = {}

        this_theme = Theme.objects.get(id = category)
        context["theme"] = this_theme
        context["pubs"] = []
        for pub_id in this_theme.get_pub_ids():
            context["pubs"].append(Article.objects.get(id=int(pub_id)))

        if self.request.user.is_superuser:
            keywords_to_context(this_theme, context)

        return render(request, self.template_name, context)

    def post(self, request, category):

        if self.request.user.is_superuser:
            this_theme = Theme.objects.get(id = category)
            update_object_KWL(this_theme, request, 100)
            return HttpResponseRedirect(reverse('userprofile_private_view'))
        raise Http404()


# class WorkpackagesListView(ListView):
#     ''''''
#     model = WorkPackage
#     template_name = 'workpackages/workpackages_list.html'


# class WorkpackagesCategoryView(ListView):
#     ''''''
#     model = Theme
#     template_name = 'workpackages/category_view.html'

#     def category(self):
#         return self.kwargs['category']

# class WorkpackagesDetailView(DetailView):
#     ''''''
#     model = Theme
#     slug_field = 'title'
#     slug_url_kwarg = 'title'
#     template_name = 'workpackages/theme_view.html'
