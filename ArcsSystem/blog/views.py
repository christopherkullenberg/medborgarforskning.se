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

class blog_list_view(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    '''
    blog = Post.objects.get(id=1)
    context = {
        'blog_title' : blog.title,
        'blog_published': blog.published,
        'blog_content' : blog.content,
        'blog_tags' : blog.tags,
    }

    return render(request, 'blog/blog_list.html', context)
    '''

class blog_detail_view(DetailView):
    template_name = 'blog/blog_detail.html'
    queryset = Post.objects.all()
    '''
    blog = Post.objects.get(id)
    context = {
        'blog_title' : blog.title,
        'blog_published': blog.published,
        'blog_content' : blog.content,
        'blog_tags' : blog.tags,
    }
    return render(request, 'blog/blog_detail.html', context)
    '''
