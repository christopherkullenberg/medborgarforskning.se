from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from staticpages.models import Page
from django.db.models import Q

class StaticDetailView(DetailView):
    model = Page
    template_name = 'staticpages/static_variant2.html'


class PageListView(ListView):
    model = Page
    template_name = 'staticpages/staticpage_list.html'



class TreeView(ListView):
    model = Page

    def get_categories():
        object_list = Page.objects.all().order_by('category')
        return object_list


class CategoryView(ListView):
    model = Page
    template_name = 'staticpages/category_list.html'

    def get_category(query):
        object_list = Page.objects.filter(
            Q(category__icontains=query)).distinct()
        return object_list
class HomePageView(TemplateView):
    template_name = 'home.html'

class TermsPageView(TemplateView):
    template_name = 'staticpages/terms-cookies-privacy_detail.html'
