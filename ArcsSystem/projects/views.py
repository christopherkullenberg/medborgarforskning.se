from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
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

from django.forms.models import model_to_dict
from django.http import Http404


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
#def project_list_view(request):
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
        return get_object_or_404(ProjectEntry, id=pk)

    def get_table_data(self):
        return [self.object]

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or int(self.request.user.id) == int(self.kwargs["pk"]):
            context['edit'] = True
        return context


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

def ProjectSubmissionView(request, pk):

    template_name = 'projects/project_detail.html'
    context = {}

    # new page : get page
    if request.method == "GET":
        if request.user.is_authenticated:
            pro_sub = ProjectSubmission.objects.get(id= pk)
            if int(request.user.id) == pro_sub.created_by.id or request.user.is_superuser:
                context = {"object": pro_sub}
                return render(request, template_name, context)
            else:
                raise Http404
    raise Http404

# edit part here

def ProjectEditView(request, pk):
    template_name = 'projects/project_submissionform.html'

    # new page : get page
    if request.method == "GET":
        if request.user.is_authenticated:
            project = ProjectEntry.objects.get(id=pk)
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                context = {"Submission": InitialProjectSubmissionModelForm(initial = model_to_dict(project))}

                return render(request, template_name, context)
            else:
                raise Http404


    #this is the save sub-form part
    if request.method == "POST":
        #check if user
        if request.user.is_authenticated:
            project = get_object_or_404(ProjectEntry, id=pk)
            form = InitialProjectSubmissionModelForm(request.POST, request.FILES, instance=project)
            # for not valid then stop
            if not form.is_valid():
                raise Http404
            # if user it the owner or admin
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                form.save()
                return HttpResponseRedirect(reverse('userprofile_private_view'))
            # else stop
            else:
                raise Http404
    raise Http404

def ProjectSubmissionEditView(request, pk):
    template_name = 'projects/project_submissionform.html'


    # new page : get page
    if request.method == "GET":
        if request.user.is_authenticated:
            project = ProjectSubmission.objects.get(id=pk)
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                context = {"Submission": InitialProjectSubmissionModelForm(initial = model_to_dict(project))}
                return render(request, template_name, context)
            else:
                raise Http404

    #this is the save sub-form part
    if request.method == "POST":
        #check if user
        if request.user.is_authenticated:
            project = get_object_or_404(ProjectSubmission, id=pk)
            form = InitialProjectSubmissionModelForm(request.POST, request.FILES, instance=project)
            # for not valid then stop
            if not form.is_valid():
                raise Http404
            # if user it the owner or admin
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                form.save()
                return HttpResponseRedirect(reverse('userprofile_private_view'))
            # else stop
            else:
                raise Http404
    raise Http404


def ProjectSubmissionCreateView(request):

    template_name = 'projects/project_submissionform.html'
    context = {}

    # new page : get page
    if request.method == "GET":
        if request.user.is_authenticated:
            keywords = {
            "contact_email": request.user.email, 
            "contact_name": request.user.first_name + " " + request.user.last_name, 
            }

            context["Submission"] = InitialProjectSubmissionModelForm(keywords)

        return render(request, template_name, context)

    # this is the save sub-form part
    if request.method == "POST":
        #check if user
        if request.user.is_authenticated:
            form = InitialProjectSubmissionModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.created_by = request.user
                form.save()
                return HttpResponseRedirect(reverse('userprofile_private_view'))
            else:


                raise Http404

# class ProjectSubmissionCreateView_old(CreateView):
#     template_name = 'projects/project_submissionform.html'
#     form_class = InitialProjectSubmissionModelForm


#     queryset = ProjectSubmission.objects.all()
#     # success_url = '/submitted-for-review' # overrides the get_absolute_url function in the model #default is project detail view - unpublished projects can be viewed until approved then can be edited once published.

#     def get_object(self):
#         pk = self.kwargs.get("pk")
#         return get_object_or_404(Project, id=pk)

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.save()
#         return super(ProjectSubmissionCreateView, self).form_valid(form)

class ProjectUpdateView(UpdateView):
    template_name = 'projects/project_submissionform.html'
    form_class = ProjectEntryUpdateManagementForm
    queryset = ProjectEntry.objects.all()
    # success_url = '/submitted-for-review' # overrides the get_absolute_url function in the model #default is project detail view - unpublished projects can be viewed until approved then can be edited once published.

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)
