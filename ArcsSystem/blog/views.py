from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils import translation
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import DateDetailView
from blog.models import (Author,
                         Post,
                         )
from django.db.models import Q



class BlogPostListView(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "publishedDate"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts



class BlogPostDetailView(DetailView):
    ''' View showing the posts itself.
    '''
    template_name = 'blog/blog_detail.html'
    queryset = Post.objects.all()

class BlogPostDateDetailView(DateDetailView):
    ''' View showing the posts itself.
    '''
    template_name = 'blog/blog_detail.html'
    object_list = Post.objects.all()
    make_object_list = True
    allow_future = True

class BlogPostIndexView(ArchiveIndexView):
    ''' View showing all the blog posts and can be paginated to beginning of time.
    '''
    template_name = 'blog/blog_list.html'
    # we need to set another solution to check language on website
    queryset = Post.objects.all()
    date_field = "publishedDate"
    make_object_list = True
    allow_future = True
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts


class BlogPostYearArchiveView(YearArchiveView):
    ''' View showing all the blog posts of a year sepecified in the url with pagination through all history.
    '''
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "publishedDate"
    make_object_list = True
    allow_future = True
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts


class BlogPostMonthArchiveView(MonthArchiveView):
    ''' View showing all the blog posts of a month based on month and year sepecified in the url with pagination through all history.
    '''
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "publishedDate"
    allow_future = True
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts

class BlogPostDayArchiveView(DayArchiveView):
    ''' View showing all the blog posts of a day sepecified in the url with pagination through all history.
    '''
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "publishedDate"
    allow_future = True
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts, bettre safe than sorry




class SearchBlogView(ListView):
    ''' View showing a list of blogs based on the search query terms.
        Search of:
        -Blog Post Title
    '''
    model = Post

    #def get_queryset(self):
    #    query = self.request.GET.get('q')
        #
    #    object_list = Article.objects.filter(
    #        Q(title__icontains=query) |
    #        Q(keywords__keyword__icontains=query) |
    #        Q(abstract__icontains=query)
    #        ).distinct()
    #    return object_list

    def get_queryset_template(number):
        object_list = Post.objects.all().distinct()[:number]
        return object_list
