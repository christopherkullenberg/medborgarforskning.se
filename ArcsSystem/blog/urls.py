from django.urls import path
from .views import blog_list_view

from .views import blog_detail_view
from django.views.generic.dates import DateDetailView
from django.views.generic.dates import ArchiveIndexView
from .models import Post

app_name = 'blog'

urlpatterns = [
    path('', ArchiveIndexView.as_view(model=Post, date_field="published"), name='blog_list_view'),
    path('<int:pk>/', blog_detail_view.as_view(), name='blog_detail_view'),
    path('<int:year>/<str:month>/<int:day>/<int:pk>/',
         DateDetailView.as_view(model=Post, date_field="published"),
         name="archive_date_detail"),
    #path('blog/<int:year>/<int:month>/<int:day>/<title:title>/',
    #     blog_detail_view,
    #     name='blog_detail'),
]
