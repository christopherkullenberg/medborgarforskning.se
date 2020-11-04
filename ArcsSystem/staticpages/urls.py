from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.urls import re_path
from .views import StaticDetailView
from .views import HomePageView
from .views import TermsPageView
from .views import StaticPages
from .views import PressPostIndexView
from .views import PressPostDateDetailView
from .views import PressPostYearArchiveView
from .views import PressPostMonthArchiveView
from .views import SearchView
from staticpages.models import PressPage

from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'staticpages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage_view'),
    # Special Static Page Views
    path('<slug:category>/<slug:slug>/', StaticPages.as_view(), name='static_pages'),
    path('terms/', TermsPageView.as_view(), name='terms_detail'),

    path('press/', PressPostIndexView.as_view(model=PressPage), name='press_list'), # the press/ view will be static parent to press related subpages
    path('press/<int:year>/',
        PressPostYearArchiveView.as_view(),name="archive_year_numeric"),
    # Example: /2020/04/
    path('press/<int:year>/<int:month>/',
        PressPostMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
    path('press/<int:year>/<str:month>/<int:day>/<slug:slug>/', PressPostDateDetailView.as_view(model=PressPage, date_field="pressPublishedDate", month_format='%m'), name="archive_date_detail"), # the press/ view will be static parent to press related subpages
    #path('contact/', .as_view(), name='contact_form'), # this is a contact form - standard for the site
    path('search/<str:query>', SearchView.as_view(), name='super_search_results')
    ]
