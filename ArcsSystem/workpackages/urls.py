from django.urls import path
from django.urls import re_path
from django.conf.urls import url
from .views import WorkpackagesListView, WorkpackagesThemeView, ajax_function

app_name = 'workpackages'

urlpatterns = [
    # generic static page views
    path('', WorkpackagesListView.as_view(), name='category_view'),
    path('ajax/', ajax_function, name='ajax_get_trans'),
    path('<int:category>/', WorkpackagesThemeView.as_view(), name='theme_view'),
]
