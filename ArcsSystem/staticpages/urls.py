from django.urls import path
from django.urls import re_path
from .views import StaticDetailView
from .views import PageListView
from .views import HomePageView
from .views import TermsPageView
from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'staticpages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage_view'),
    # Special Static Page Views
    path('terms/', TermsPageView.as_view(), name='terms_detail'),
    path('privacy/cookies/', TermsPageView.as_view(), name='cookies_detail'),
    path('privacy/', TermsPageView.as_view(), name='privacy_detail'),
    path('privacy/', TermsPageView.as_view(), name='privacy_detail'),
    path('sourcecode/', TermsPageView.as_view(), name='sourcecode_detail'),

    # generic static page views
    path('resources/', PageListView.as_view(), name='staticpage_list'),
    path('resources/<slug:slug>/', StaticDetailView.as_view(), name='staticpage'),

    ]
