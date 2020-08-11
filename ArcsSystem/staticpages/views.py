from django.shortcuts import render
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
from staticpages.models import (HomePage,
                                TermsPage,
                                PrivacyPage,
                                SourcecodePage,
                                PressPage)
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
    def get_context_data(self, **kwargs):
        try:
            model = HomePage.objects.prefetch_related('welcome_image')[0]
        except :
            model = None
        context = super().get_context_data(**kwargs)
        context["page"] = model
        return context

class TermsPageView(TemplateView):
    template_name = 'staticpages/terms-cookies-privacy_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["termpage"] = TermsPage.objects.all()
        return context

class PrivacyPageView(TemplateView):
    template_name = 'staticpages/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["privacypage"] = PrivacyPage.objects.all()
        return context

class SourcecodePageView(TemplateView):
    template_name = 'staticpages/source_code.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sourceodepage"] = SourcecodePage.objects.all()
        return context


class PressPostDateDetailView(DateDetailView):
    template_name = 'staticpages/press_detail.html'
    model = PressPage
    queryset = PressPage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class PressPostIndexView(ArchiveIndexView):
    template_name = 'staticpages/press_list.html'
    queryset = PressPage.objects.all()
    date_field = "pressPublishedDate"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 5    # Change this to include more posts

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
