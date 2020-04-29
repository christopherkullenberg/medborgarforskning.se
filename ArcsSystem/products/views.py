from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from products.models import Product
from products.models import Article
from products.models import Arcsreport
from django.db.models import Q




class ProductListView(ListView):
    '''
    '''
    model = Product
    template_name = 'products/product_list.html'


class ProductDetailView(DetailView):
    '''
    '''
    model = Article
    template_name = 'products/product_detail.html'


class ArticleDetailView(DetailView):
    '''
    '''
    model = Article
    template_name = 'products/article_detail.html'

class ArcsreportDetailView(DetailView):
    '''
    '''
    model = Article
    template_name = 'products/arcsreport_detail.html'


class SearchResultsView(ListView):
    model = Product
    template_name = 'products/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #
        object_list = Product.objects.filter(
            Q(title__icontains=query) |
            Q(keywords__keyword__icontains=query) |
            Q(abstract__icontains=query
            ))
        return object_list
