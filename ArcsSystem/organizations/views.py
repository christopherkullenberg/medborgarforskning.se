from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from organizations.models import Organization
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

class OrganiztionList(ListView):
    model = Organization
    template_name = 'organizations/organization_list.html'
    queryset = Organization.objects.all()

class OrganizationDetailView(DetailView):

    model = Organization
    template_name = 'organizations/organization_detail.html'
