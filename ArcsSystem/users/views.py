from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

class UserProfilePageView(TemplateView):
    template_name = "users/profile.html"
    # TODO add access control to view - https://docs.djangoproject.com/en/2.2/topics/auth/default/#permissions-and-authorization
