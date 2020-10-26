from django.urls import path
from .views import KeywordList
from .views import keywordDetailView

app_name = 'keywords'

urlpatterns = [
    path('', KeywordList.as_view(),
        name ='keyword_list'),
    path('<str:name>/', keywordDetailView,
        name = 'keyword_detail')
]
