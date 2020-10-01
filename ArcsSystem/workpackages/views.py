from django.shortcuts import render
from django.views.generic import DetailView, ListView
from workpackages.models import WorkPackage, Theme
from django.views import View

from .models import Theme, WorkPackage
from publications.models import Article
# Create your views here.


# this is the view for the workpack home_page
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

        this_theme = Theme.objects.get(title = category)
        context = {"theme": this_theme}
        context["pubs"] = []
        for pub_id in this_theme.get_pub_ids():
            context["pubs"].append(Article.objects.get(id=int(pub_id)))
            
        return render(request, self.template_name, context)


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
