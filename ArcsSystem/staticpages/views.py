from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DateDetailView

from staticpages.models import Page
from staticpages.models import (
                                TermsPage,
                                PressPage,)
from django.db.models import Q

class StaticDetailView(DetailView):
    model = Page
    template_name = 'staticpages/static_variant2.html'


class HomePageView(TemplateView):

    template_name = 'home.html'

class StaticPages(DetailView):

    template_name = 'staticpages/staticpage.html'
    model =  Page

    def get_page(u):
        object_list = Page.objects.filter(Q(slug__icontains=u))
        return object_list

    def get_menu(cat):
        object_list = Page.objects.filter(Q(category__icontains=cat))
        return object_list

class TermsPageView(TemplateView):
    template_name = 'staticpages/terms-cookies-privacy_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["termpage"] = TermsPage.objects.all()
        return context


class PressPostIndexView(ArchiveIndexView):
    template_name = 'staticpages/press_list.html'
    queryset = PressPage.objects.all()
    date_field = "pressPublishedDate"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts


class PressPostDateDetailView(DateDetailView):
    template_name = 'staticpages/press_detail.html'
    object_list = PressPage.objects.all()
    make_object_list = True
    allow_future = True


class PressPostYearArchiveView(YearArchiveView):
    template_name = 'staticpages/press_detail.html'
    queryset = PressPage.objects.all()
    date_field = "pressPublishedDate"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 5    # Change this to include more posts


class PressPostMonthArchiveView(MonthArchiveView):
    template_name = 'staticpages/press_detail.html'
    queryset = PressPage.objects.all()
    date_field = "pressPublishedDate"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 5    # Change this to include more posts
