from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView

from publications.models import Article
from workpackages.models import WorkPackage, Theme
from django import forms

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q

# forms is here

class Asing_theme_form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.cat = kwargs.pop('cat')
        cat_id = kwargs.pop('cat_id')
        pub_id = kwargs.pop('pub_id')
        super(Asing_theme_form, self).__init__(*args, **kwargs)

        for th in Theme.objects.filter(wp_parent=cat_id):

            if str(pub_id) in th.get_pub_ids():
                field = forms.BooleanField(label=th.title, required=False, initial=True)
            else:
                field = forms.BooleanField(label=th.title, required=False)
            field.widget.attrs['class'] = "form-control col-md-4"

            self.fields[str(th.id)] = field
            


# forms end here

def ChangeThemePub(request):

    if request.user.is_superuser:
        if request.method == "GET":
            pub_id = request.GET["pub_id"]
            for th in Theme.objects.all():
                pub_ids = th.get_pub_ids()
                th_id = str(th.id)
                # if box is checked 
                if th_id in request.GET:
                    # and pub_id not in theme
                    if pub_id not in pub_ids:
                        # then add pub_id
                        th.save_pub_ids(pub_ids + [pub_id])   
                # if box in not checked
                else:
                    # and pub id in theme
                    if pub_id in pub_ids:
                        # then remove pub_id
                        pub_ids.remove(pub_id)
                        th.save_pub_ids(pub_ids)

    return HttpResponseRedirect(reverse('publications:article_publications_list'))




class ArticleListView(ListView):
    '''
    '''
    model = Article
    template_name = 'publications/article_publications_list.html'
    queryset = Article.objects.order_by('-py')[:20]


class ArticleDetailView(DetailView):
    '''
    '''


    model = Article
    template_name = 'publications/article_publications_detail.html'



    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['forms'] = [Asing_theme_form( cat_id = cat.id, cat= cat, pub_id = self.kwargs['pk']) for cat  in WorkPackage.objects.all() ]
        return context

class SearchPublicationsView(ListView):
    model = Article
    template_name = 'publications/search_publications_results.html'


    def get_queryset(self):
        query = self.request.GET.get('q')
        sortmethod = self.request.GET.get('sortmethod')
        if sortmethod == "year":
            orderquery = "py"
        elif sortmethod == "title":
            orderquery = "title"
        else:
            orderquery = "authors"

        object_list = Article.objects.filter(
            Q(title_en__icontains=query) |
            Q(keywords__keyword__icontains=query) |
            Q(abstract_en__icontains=query)
            ).distinct().order_by(orderquery)
        return object_list

    def get_queryset_template(query):
        object_list = Article.objects.filter(
            Q(title_en__icontains=query) |
            Q(keywords__keyword__icontains=query) |
            Q(abstract_en__icontains=query)
            ).distinct()
        return object_list

    # def related_publications(query, number):
    #     object_list = Article.objects.filter(
    #         Q(title_en__icontains=query) |
    #         Q(keywords__keyword__icontains=query) |
    #         Q(abstract_en__icontains=query)
    #         ).distinct().order_by("-py")[:number]
    #     return object_list

    def related_publications(query, number):
        condition = None
        for tag in query:
            if condition:
                condition = Q(title_en__icontains=tag) | Q(keywords__keyword__icontains=tag) | Q(abstract_en__icontains=tag) | condition
            else:
                condition = Q(title_en__icontains=tag) | Q(keywords__keyword__icontains=tag) | Q(abstract_en__icontains=tag)
        object_list = Article.objects.filter(condition).distinct().order_by("-py")[:number]
        return object_list

    def recent_publications(number):
        object_list = Article.objects.all().distinct().order_by("-py")[:number]
        return object_list
