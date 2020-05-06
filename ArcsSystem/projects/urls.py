from django.urls import path
from .views import ProjectDetailView
from .views import ProjectListView
from .views import SearchResultsView
from .views import ProjectSubmissionCreateView

#from .views import #insertviewname

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(),
        name='project_list'),
    path('add/', ProjectSubmissionCreateView.as_view(), # CK previous attempt TODO replacing with CreateView
         name='project_submissionform' ),
    path('<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),
    path('search/', SearchResultsView.as_view(),
         name ='search_results'),

]
