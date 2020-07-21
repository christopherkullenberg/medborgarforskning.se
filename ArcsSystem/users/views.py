from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

class UserPrivateProfilePageView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/private_profile.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    # TODO add access control to view - https://docs.djangoproject.com/en/2.2/topics/auth/default/#permissions-and-authorization

class UserPublicProfilePageView(TemplateView):
    model = CustomUser
    template_name = "users/public_profile.html"
    # TODO add access control to view - https://docs.djangoproject.com/en/2.2/topics/auth/default/#permissions-and-authorization
