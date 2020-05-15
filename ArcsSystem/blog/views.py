from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DayArchiveView
from blog.models import (Author,
                         Post
                         )
from django.db.models import Q
#from products.models import Product
#from projects.models import Project



class BlogPostListView(ListView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()

class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class BlogPostIndexView(ArchiveIndexView):
    ''' This view to shows all the publications and can be paginated to beginning of time.
    '''
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "published"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts

class BlogPostYearArchiveView(YearArchiveView):
    ''' This view show all the publications with pagination to tab through the history of the year in the URL.
    '''
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "published"
    make_object_list = True
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts

class BlogPostMonthArchiveView(MonthArchiveView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "published"
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts

class BlogPostDayArchiveView(DayArchiveView):
    template_name = 'blog/blog_list.html'
    queryset = Post.objects.all()
    date_field = "published"
    allow_future = False
    # Pagination documentation https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginate_by = 3    # Change this to include more posts, bettre safe than sorry 

class SearchBlogView(ListView):
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

    def get_queryset_template(query):
        object_list = Post.objects.filter(
            Q(title__icontains=query)).distinct()
        return object_list
