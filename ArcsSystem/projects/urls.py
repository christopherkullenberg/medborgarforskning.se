from django.urls import path
#from .views import project_detail_view
#from .views import project_list_view
from .views import ProjectDetailView
from .views import ProjectListView
from .views import ProjectSubmitView

#from .views import #insertviewname



urlpatterns = [
    path('', ProjectListView.as_view(),
        name='project_list'),
    path('add/', ProjectSubmitView.as_view(),
        name='project_submissionform' ),
    path('<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),

]
