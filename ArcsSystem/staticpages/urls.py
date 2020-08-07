from django.urls import path
from django.urls import re_path
from .views import StaticDetailView
from .views import PageListView
from .views import CategoryView
from .views import HomePageView
from .views import TermsPageView
from .views import PrivacyPageView
from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'staticpages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage_view'),
    # Special Static Page Views
    path('terms/', TermsPageView.as_view(), name='terms_detail'),
    path('privacy/cookies/', TermsPageView.as_view(), name='cookies_detail'),
    path('privacy/', PrivacyPageView.as_view(), name='privacy_detail'),
    path('sourcecode/', TermsPageView.as_view(), name='sourcecode_detail'),
    path('press/', TermsPageView.as_view(), name='press_detail'), # the press/ view will be static parent to press related subpages
    #path('contact/', .as_view(), name='contact_form'), # this is a contact form - standard for the site
    ]
