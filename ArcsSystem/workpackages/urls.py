from django.urls import path
from django.urls import re_path
from .views import WorkpackagesListView
from .views import WorkpackagesCategoryView
from .views import WorkpackagesDetailView


from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'workpackages'

urlpatterns = [
    # generic static page views
    path('', WorkpackagesListView.as_view(), name='workpackages_list'),
    path('<slug:category>/', WorkpackagesCategoryView.as_view(), name='category_view'),
    path('<slug:category>/<slug:title>/', WorkpackagesDetailView.as_view(), name='theme_view'),
]
