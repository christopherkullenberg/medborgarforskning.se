from django.urls import path
from .views import blog_list_view
from .views import blog_detail_view


urlpatterns = [
    path('', blog_list_view),
    #path('blog/<int:year>/<int:month>/<int:day>/<title:title>/',
    #     blog_detail_view,
    #     name='blog_detail'),
]
