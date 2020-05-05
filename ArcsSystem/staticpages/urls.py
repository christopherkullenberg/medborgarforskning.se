from django.urls import path
from django.urls import re_path
from .views import StaticDetailView
from .views import PageListView
from django.views.generic.dates import DateDetailView
from staticpages.models import Page

app_name = 'staticpages'

urlpatterns = [
    path('', PageListView.as_view(),
    name='staticpage_list'),
    path('<slug:slug>/', StaticDetailView.as_view(), name='staticpage'),
    # Example: /2020/
    #path('<str:slug>/', StaticDetailView.as_view()),
    #re_path(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/$', DateDetailView.as_view(model=Post, date_field="published"),name="archive_date_detail"),
    ]
