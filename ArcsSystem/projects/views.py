from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from projects.models import ProjectEntry, ProjectSubmission
from django.db.models import Q

from .forms import (
    InitialProjectSubmissionModelForm,
    ProjectEntryUpdateManagementForm
)

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
    model = ProjectEntry
    template_name = 'projects/project_list.html'

    # def project_list_view(request):
    #    project_list = Project.objects.all()
    #    context = {
    #        'project_list' : project_list,
    #    }
    #    return render(request, 'project_list.html', context)


class ProjectDetailView(DetailView):
    '''
    '''
    model = ProjectEntry
    template_name = 'projects/project_detail.html'

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)


class SearchResultsView(ListView):
    model = ProjectEntry
    template_name = 'projects/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #
        object_list = Project.objects.filter(
            Q(name__icontains=query) | Q(keywords__keyword__icontains=query)
        ).distinct()
        return object_list


class StaticKeywordView(ListView):
    model = ProjectEntry
    template_name = 'projects/search_results_pure.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #
        object_list = ProjectEntry.objects.filter(
            Q(name__icontains=query) | Q(keywords__keyword__icontains=query)
        ).distinct()
        return object_list

class ProjectSubmissionCreateView(CreateView):
    template_name = 'projects/project_submissionform.html'
    form_class = InitialProjectSubmissionModelForm
    queryset = ProjectSubmission.objects.all()
    # success_url = '/submitted-for-review' # overrides the get_absolute_url function in the model #default is project detail view - unpublished projects can be viewed until approved then can be edited once published.

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)

class ProjectUpdateView(UpdateView):
    template_name = 'projects/project_submissionform.html'
    form_class = ProjectEntryUpdateManagementForm
    queryset = ProjectEntry.objects.all()
    # success_url = '/submitted-for-review' # overrides the get_absolute_url function in the model #default is project detail view - unpublished projects can be viewed until approved then can be edited once published.

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)
