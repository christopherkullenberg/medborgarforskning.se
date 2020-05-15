from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from staticpages.models import Page

class StaticDetailView(DetailView):
    model = Page
    template_name = 'staticpages/static_variant2.html'


class PageListView(ListView):
    model = Page
    template_name = 'staticpages/staticpage_list.html'

class HomePageView(TemplateView):
    template_name = 'staticpages/main-page.html'

class TermsPageView(TemplateView):
    template_name = 'staticpages/terms-cookies-privacy_detail.html'
