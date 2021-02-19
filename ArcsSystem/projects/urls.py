from django.urls import path
from .views import ProjectDetailView
from .views import ProjectListView
from .views import SearchResultsView
from .views import ProjectSubmissionCreateView
from .views import ProjectSubmissionView
from .views import ProjectEditView
from .views import ProjectSubmissionEditView
from .views import ProjectListViewFilter
from .views import GetEUAPI


#from .views import #insertviewname

app_name = 'projects'

urlpatterns = [
    path('', GetEUAPI.as_view(),
        name='project_list'),

    path('filter/', ProjectListViewFilter,
        name='project_list_filter'),

    path('add/', ProjectSubmissionCreateView, # CK previous attempt TODO replacing with CreateView
         name='project_submissionform' ),

    # show pro
    path('<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),

    # edit my pro
    path('<int:pk>/edit/', ProjectEditView,
        name='project_edit'),

    # show my sub
    path('project_submission/<int:pk>/', ProjectSubmissionView,
        name='project_submission_detail'),

    # edit my sub
    path('project_submission/<int:pk>/edit/', ProjectSubmissionEditView,
        name='project_submission_edit'),

    path('search/', SearchResultsView.as_view(),
         name ='search_results'),

]
