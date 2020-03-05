from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Blog, Author
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

def home_view(request):
    '''
    '''
    blog = Blog.objects.get(id=1)
    product = Product.objects.get(id=1)
    project = Project.objects.get(id=1)
    context = {
        'blog_name' : blog.name,
        'blog_tagline' : blog.tagline,
        'product_title' : product.title,
        'project_name': project.name,
    }
    return render(request, 'home.html', context)

def blog_detail_view(request):
    '''
    '''
    blog = Blog.objects.get(id=1)
    context = {
        'blog_name' : blog.name,
        'blog_tagline' : blog.tagline,
    }
    return render(request, 'blog/blog_detail.html', context)
