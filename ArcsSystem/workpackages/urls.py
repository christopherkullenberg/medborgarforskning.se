from django.urls import path
from django.urls import re_path
from django.conf.urls import url
from .views import WorkpackagesListView, WorkpackagesThemeView



from django.views.generic.dates import DateDetailView
#from staticpages.models import Page

app_name = 'workpackages'

# urlpatterns = [
#     # generic static page views
#     path('', WorkpackagesListView.as_view(), name='workpackages_list'),
#     path('<slug:category>/', WorkpackagesCategoryView.as_view(), name='category_view'),
#     path('<slug:category>/<slug:title>/', WorkpackagesDetailView.as_view(), name='theme_view'),
# ]


urlpatterns = [
    # generic static page views
    path('', WorkpackagesListView.as_view(), name='category_view'),
    # path('<slug:category>/', WorkpackagesCategoryView.as_view()),
    path('<int:category>/', WorkpackagesThemeView.as_view(), name='theme_view'),

]
