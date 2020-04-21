from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Author, Post
from products.models import Product
from projects.models import Project

'''
# Quick Fuction based template
def template_view(request):
'''
'''
    context = {
        }
    return render(request, 'exampletemplate.html', context)
'''

def blog_list_view(request):
    '''
    '''
    blog = Post.objects.get(id=1)
    context = {
        'blog_title' : blog.title,
        'blog_published': blog.published,
        'blog_content' : blog.content,
        'blog_tags' : blog.tags,
        #'product_title' : product.title,
        #'project_name': project.name,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail_view(request):
    '''
    '''
    blog = Post.objects.get(id=1)
    context = {
        'blog_title' : blog.title,
        'blog_published': blog.published,
        'blog_content' : blog.content,
        'blog_tags' : blog.tags,
    }
    return render(request, 'blog/blog_detail.html', context)
