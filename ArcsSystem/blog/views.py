from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from blog.models import (Author,
                         Post
                         )
from products.models import Product
from projects.models import Project


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()

class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    queryset = Post.objects.all()

class ArchiveIndexView(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
