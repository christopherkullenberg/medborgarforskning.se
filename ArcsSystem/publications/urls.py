from django.urls import path
from .views import ArticleListView
#from .views import ProductDetailView
from .views import ArticleDetailView
#from .views import ArcsreportDetailView
from .views import SearchPublicationsView

from .views import ChangeThemePub

app_name = 'publications'

urlpatterns = [
    path('', ArticleListView.as_view(),
        name='article_publications_list'),
    #path('<int:pk>/', ProductDetailView.as_view(),
    #    name='product_detail'),
    path('<int:pk>/', ArticleDetailView.as_view(),
        name='article_publications_detail'),
    #path('arcsreport/<int:pk>/', ArcsreportDetailView.as_view(),
    #        name='arcsreport_detail'),
    path('search', SearchPublicationsView.as_view(),
         name ='search_publications_results'),

    path('admin_change', ChangeThemePub,
         name ='admin_change'),

]
