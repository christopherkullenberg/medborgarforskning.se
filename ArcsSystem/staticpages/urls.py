from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.urls import re_path
from .views import StaticDetailView
from .views import PageListView
from .views import CategoryView
from .views import HomePageView
from .views import TermsPageView
from .views import PrivacyPageView
from .views import PressPostIndexView
from .views import PressPostDateDetailView
from .views import SourcecodePageView
from .views import PressPostYearArchiveView
from .views import PressPostMonthArchiveView
from .views import GettingStartedwithCitizenScience
from .views import WhatsCitizenScience
from .views import SwedishCitizenScience
from .views import GetSubmenu
from staticpages.models import PressPage

from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'staticpages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage_view'),
    # Special Static Page Views
    path('terms/', TermsPageView.as_view(), name='terms_detail'),
    path('privacy/cookies/', TermsPageView.as_view(), name='cookies_detail'),
    path('privacy/', PrivacyPageView.as_view(), name='privacy_detail'),
    path('sourcecode/', SourcecodePageView.as_view(), name='sourcecode_detail'),
    path('press/', PressPostIndexView.as_view(model=PressPage), name='press_list'), # the press/ view will be static parent to press related subpages
    path('<int:year>/',
        PressPostYearArchiveView.as_view(),name="archive_year_numeric"),
    # Example: /2020/04/
    path('<int:year>/<int:month>/',
        PressPostMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
    path('<int:year>/<str:month>/<int:day>/<slug:slug>/', PressPostDateDetailView.as_view(model=PressPage, date_field="pressPublishedDate", month_format='%m'), name="archive_date_detail"), # the press/ view will be static parent to press related subpages
    #path('contact/', .as_view(), name='contact_form'), # this is a contact form - standard for the site
    path('<slug:title>/', GettingStartedwithCitizenScience.as_view(), name='getting_started'),
    path('<slug:title>/<slug:title2>', GetSubmenu.as_view(), name='submenu'),
    path('<slug:title>/<slug:title2>/<slug:title3>/', SwedishCitizenScience.as_view(), name='getting_started_swedish_citizen_science')
    ]
