from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from projects.models import Project
from django.db.models import Q

'''
# Quick Fuction based template
def template_view(request):
'''
'''
    context = {
        }
    return render(request, 'exampletemplate.html', context)
'''

# Create your views here.

class ProjectListView(ListView):
    '''
    '''
    model = Project
    template_name = 'projects/project_list.html'
#def project_list_view(request):
#    project_list = Project.objects.all()
#    context = {
#        'project_list' : project_list,
#    }
#    return render(request, 'project_list.html', context)


class ProjectDetailView(DetailView):
    '''
    '''
    model = Project
    template_name = 'projects/project_detail.html'



class ProjectSubmitView(DetailView):
    '''
    This is not working, dont know how to make logged in user (CK)
    '''
    model = Project
    template_name = 'projects/project_submissionform.html'
    # def get_object(self):
    #     return get_object_or_404(User, pk=request.session['user_id'])


class SearchResultsView(ListView):
    model = Project
    template_name = 'projects/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #
        object_list = Project.objects.filter(
            Q(name__icontains=query) | Q(keywords__keyword__icontains=query)
        )
        return object_list
