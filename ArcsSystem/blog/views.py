from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Author, Post
from products.models import Product
from projects.models import Project


class blog_list_view(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()


class blog_detail_view(DetailView):
    template_name = 'blog/blog_detail.html'
    queryset = Post.objects.all()
