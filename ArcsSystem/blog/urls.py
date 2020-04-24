from django.urls import path
from django.urls import re_path
from blog.views import BlogListView
from blog.views import BlogDetailView
from django.views.generic.dates import DateDetailView
from django.views.generic.dates import ArchiveIndexView
from blog.models import Post

app_name = 'blog'

urlpatterns = [
    path('', ArchiveIndexView.as_view(model=Post, date_field="published"), name='blog_list_view'),
    path('<int:year>/<str:month>/<int:day>/<int:pk>/', DateDetailView.as_view(model=Post, date_field="published"),name="archive_date_detail"),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail_view'),
    ]
