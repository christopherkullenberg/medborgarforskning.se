from django.urls import path
from publications.views import ArticleListView
#from .views import ProductDetailView
from publications.views import ArticleDetailView
#from .views import ArcsreportDetailView
from publications.views import SearchPublicationsView

app_name = 'publications'

urlpatterns = [
    path('', ArticleListView.as_view(),
        name='article_publication_list'),
    #path('<int:pk>/', ProductDetailView.as_view(),
    #    name='product_detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(),
        name='article_publication_detail'),
    #path('arcsreport/<int:pk>/', ArcsreportDetailView.as_view(),
    #        name='arcsreport_detail'),
    path('search/', SearchPublicationsView.as_view(),
         name ='search_publications_results'),
]
