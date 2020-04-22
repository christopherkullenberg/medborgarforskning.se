from django.urls import path
from .views import blog_list_view
from .views import blog_detail_view

app_name = 'blog'

urlpatterns = [
    path('', blog_list_view.as_view(), name='blog_list_view'),
    path('<int:pk>/', blog_detail_view.as_view(), name='blog_detail_view'),
    #path('blog/<int:year>/<int:month>/<int:day>/<title:title>/',
    #     blog_detail_view,
    #     name='blog_detail'),
]
