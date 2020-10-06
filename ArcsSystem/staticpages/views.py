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
from staticpages.models import (HomePage,
                                TermsPage,
                                PrivacyPage,
                                SourcecodePage,
                                PressPage,
                                CitizenSciencePage,
                                WhatsCitizenSciencePage,
                                SwedishCitizenSciencePage,
                                CaseStudiesPage,
                                FAQPage,
                                AdditionalResourcesPage)
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

class PressPostIndexView(ArchiveIndexView):
    template_name = 'staticpages/press_list.html'
    # we need to set another solution to check language on website

    # def get_context_data(self, **kwargs):
    #     language_code = translation.get_language()
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     if (language_code == 'en'):
    #         context["object_list"] = BlogPage.objects.exclude(slug_en = None)
    #     else:
    #         context["object_list"] = BlogPage.objects.exclude(slug_sv = None)
    #     return context

    queryset = PressPage.objects.all()
    date_field = "pressPublishedDate"
    make_object_list = True
    allow_future = True
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts


class PressPostDateDetailView(DateDetailView):
    template_name = 'staticpages/press_detail.html'
    model = PressPage
    queryset = PressPage.objects.all()
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


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


class WhatsCitizenScience(TemplateView):

    template_name = 'staticpages/what_is_citizen_science.html'
    # queryset = WhatsCitizenSciencePage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citizen_science"] = WhatsCitizenSciencePage.objects.all()
        return context

    def get_absolute_url(self):
        return reverse('staticpages:what_is_citizen_science')


class SwedishCitizenScience(TemplateView):
    template_name = 'staticpages/swedish_citizen_science.html'
    queryset = SwedishCitizenSciencePage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["swedish_citizen_science"] = self.queryset
        return context

    def get_absolute_url(self):
        return reverse('staticpages:swedish_citizen_science')


class CaseStudies(TemplateView):
    template_name = 'staticpages/case_studies.html'
    queryset = CaseStudiesPage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case_studies'] = self.queryset
        return context

    def get_absolute_url(self):
        return reverse('staticpages:case_studies')

class FAQ(TemplateView):
    template_name = 'staticpages/faq.html'
    queryset = FAQPage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faq"] = self.queryset
        return context

    def get_absolute_url(self):
        return reverse('staticpages:faq')


class AditionalResources(TemplateView):
    template_name = 'staticpages/additional_resources.html'
    model = AdditionalResourcesPage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_resources"] = self.model
        return context

    def get_submenu(number):
        model = AdditionalResourcesPage.objects.all()
        object_list = model.distinct()[:number]
        return object_list

    def get_absolute_url(self):
        return reverse('staticpages:additional_resources')


# class GetSubmenu(TemplateView):
#
#     template_name = 'staticpages/case_studies.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         what_is_citizen_science = WhatsCitizenSciencePage.objects.latest('id')
#         case_studies_query = CaseStudiesPage.objects.latest('id')
#         faq_query = FAQPage.objects.latest('id')
#         additional_resources_query = AdditionalResourcesPage.objects.latest('id')
#
#         if (kwargs['title2'] == what_is_citizen_science.slug):
#             return render(self.request, 'staticpages/what_is_citizen_science.html', {'citizen_science':WhatsCitizenSciencePage.objects.all()})
#         if (kwargs['title2'] == case_studies_query.slug):
#             return render(self.request, 'staticpages/case_studies.html', {'case_studies':CaseStudiesPage.objects.all()})
#         if (kwargs['title2'] == faq_query.slug):
#             return render(self.request, 'staticpages/faq.html', {'faq':FAQPage.objects.all()})
#         if (kwargs['title2'] == additional_resources_query.slug):
#             return render(self.request, 'staticpages/additional_resources.html', {'additional_resources':AdditionalResourcesPage.objects.all()})
#
#         else:
#             return redirect("/")
