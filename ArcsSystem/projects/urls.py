from django.urls import path
#from .views import project_detail_view
#from .views import project_list_view
from .views import ProjectDetailView
from .views import ProjectListView
from .views import ProjectSubmitView
from .views import SearchResultsView

#from .views import #insertviewname

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(),
        name='project_list'),
    path('add/', ProjectSubmitView.as_view(),
        name='project_submissionform' ),
    path('<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),
    path('search/', SearchResultsView.as_view(),
         name ='search_results'),

]
