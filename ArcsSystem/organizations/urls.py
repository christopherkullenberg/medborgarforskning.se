from django.urls import path
from .views import OrganiztionList
from .views import OrganizationDetailView

app_name = 'organizations'

urlpatterns = [
    path('all', OrganiztionList.as_view(),
        name ='organization_list'),
    path('<int:pk>/', OrganizationDetailView.as_view(),
        name = 'organization_detail')
]
