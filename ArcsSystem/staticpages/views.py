from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from staticpages.models import Page

class StaticDetailView(DetailView):
    model = Page
    template_name = 'staticpages/static_variant2.html'


class PageListView(ListView):
    model = Page
    template_name = 'staticpages/staticpage_list.html'
