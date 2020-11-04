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

from .models import KeywordEng, KeywordSwe, KeywordLine


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
        if self.request.user.is_authenticated:
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
                context['edit'] = True
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


                sv_list, en_list = project.get_sv_en_keywords()
                context["keyword_line"] = []
                context["keyword_len"] = len(sv_list)
                for i in range(context["keyword_len"]):
                    context["keyword_line"].append([sv_list[i], en_list[i]])

                if project.image:

                    context["inital_image"] = project.image.url

                return render(request, template_name, context)
            else:
                raise Http404


    #this is the save sub-form part
    if request.method == "POST":
        print("post")
        #check if user
        if request.user.is_authenticated:
            project = get_object_or_404(ProjectEntry, id=pk)
            form = InitialProjectSubmissionModelForm(request.POST, request.FILES, instance=project)

            # for not valid then stop
            if not form.is_valid():
                return render(request, template_name, {"Submission": form})

            print("valid")


            # if user it the owner or admin
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:

                form.instance.created_by = request.user

                update_project_entry_keyword_lines(project, * load_keywords_list(request))

                print(project.keywords)

                form.save()

                return HttpResponseRedirect(reverse('userprofile_private_view'))
            # else stop
            else:
                raise Http404
    raise Http404

def load_keywords(request):

    sve_string = ""
    eng_string = ""

    for nr in range(1, 11):
        if "Keyword_sve_" + str(nr) in request.POST or "Keyword_eng_" + str(nr) in request.POST:


            if "Keyword_sve_" + str(nr) in request.POST:
                sve_string += request.POST["Keyword_sve_" + str(nr)].replace("&", "") + "&"
            else:
                sve_string += "&"


            if "Keyword_eng_" + str(nr) in request.POST:
                eng_string += request.POST["Keyword_eng_" + str(nr)].replace("&", "") + "&"
            else:
                eng_string += "&"

        else:

            break
    return sve_string, eng_string

def remove_space(string):

    start_c = 0

    for char in string:
        if char == " ":
            start_c += 1
        else: 
            break

    end_c = 0
    for char in string[::-1]:

        if char == " ":
            end_c += 1
        else:
            break

    if end_c == 0:
        return string[start_c:None]
    return string[start_c:-1*end_c]




def load_keywords_list(request):

    sve_string = []
    eng_string = []

    for nr in range(1, 11):
        if "Keyword_sve_" + str(nr) in request.POST or "Keyword_eng_" + str(nr) in request.POST:


            if "Keyword_sve_" + str(nr) in request.POST:
                sve_string += [request.POST["Keyword_sve_" + str(nr)].replace("&", "")]
            else:
                sve_string += [""]


            if "Keyword_eng_" + str(nr) in request.POST:
                eng_string += [request.POST["Keyword_eng_" + str(nr)].replace("&", "")]
            else:
                eng_string += [""]


    return sve_string, eng_string


def ProjectSubmissionEditView(request, pk):
    template_name = 'projects/project_submissionform.html'


    # new page : get page
    if request.method == "GET":
        if request.user.is_authenticated:
            project = ProjectSubmission.objects.get(id=pk)
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                context = {"Submission": InitialProjectSubmissionModelForm(initial = model_to_dict(project))}
                
                sv_list, en_list = project.get_keywords()


                context["keyword_line"] = []
                context["keyword_len"] = len(sv_list)
                for i in range(context["keyword_len"]):
                    context["keyword_line"].append([sv_list[i], en_list[i]])

                if project.image != None:
                    context["inital_image"] = project.image.url

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
                return render(request, template_name, {"Submission": form})

            # if user it the owner or admin
            if int(request.user.id) == project.created_by.id or request.user.is_superuser:
                form.instance.created_by = request.user
                form.instance.keywords_sv, form.instance.keywords_en = load_keywords(request)
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
                form.instance.keywords_sv, form.instance.keywords_en = load_keywords(request)


                form.save()

                return HttpResponseRedirect(reverse('userprofile_private_view'))
            else:

                context["Submission"] = form


                return render(request, template_name, context)


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



def update_project_entry_keyword_lines(model, key_sv, key_en ):

    model.keywords = ""
    model.keyword_lines.clear()




    for key_sv, key_en in zip(key_sv, key_en):


        # if both are empty continue 
        if key_sv == "" and key_en == "":
            continue

        # if sv is empty but not en
        if key_sv == "":

            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()
            options = model_keyword_eng.line.filter(swe=None)

            if len(options) > 0:
                model.add_keyword(options.first())
                model.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(eng=model_keyword_eng)
                model_keyword_line.save()
                model.add_keyword(model_keyword_line)
                model.keyword_lines.add(options.first())


        # if sv is empty but not en
        elif key_en == "":

            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()
            options = model_keyword_swe.line.filter(eng=None)

            if len(options) > 0:
                model.add_keyword(options.first())
                model.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe)
                model_keyword_line.save()
                model.add_keyword(model_keyword_line)
                model.keyword_lines.add(options.first())

        # both are filed-in        
        else:

            # en key
            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()


            # sv key
            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()


            options = model_keyword_swe.line.filter(eng=model_keyword_eng)

            if len(options) > 0:
                model.add_keyword(options.first())
                model.keyword_lines.add(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe, eng=model_keyword_eng)
                model_keyword_line.save()
                model.add_keyword(model_keyword_line)
                model.keyword_lines.add(options.first())














