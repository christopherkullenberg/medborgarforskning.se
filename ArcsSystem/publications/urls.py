from django.urls import path
from .views import ArticleListView
#from .views import ProductDetailView
from .views import ArticleDetailView
#from .views import ArcsreportDetailView
from .views import SearchResultsView

app_name = 'publications'

urlpatterns = [
    path('', ArticleListView.as_view(),
        name='article_list'),
    #path('<int:pk>/', ProductDetailView.as_view(),
    #    name='product_detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(),
        name='article_detail'),
    #path('arcsreport/<int:pk>/', ArcsreportDetailView.as_view(),
    #        name='arcsreport_detail'),
    path('results/', SearchResultsView.as_view(), name ='search_results'),
]
