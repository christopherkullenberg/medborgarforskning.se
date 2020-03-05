from django.shortcuts import render

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
def organization_detail_view(request):
''' This view shows which organizations are included in the database. It can
be extended with content of papers, researchers, etc that are associated with
the organization via relationships in the database.
'''
    context = {
        }
    return render(request, 'organization_detail.html', context)
