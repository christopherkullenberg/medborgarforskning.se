from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomUserPrivateForm
from django import forms
from staticpages.models import TermsPage
from django.contrib.auth import logout
from datetime import date

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

class UserPublicProfilePageView(DetailView):
    template_name = 'users/public_profile_view.html'

    def get_object(self, queryset=None):
        obj = None
        if "username" in self.kwargs.keys():
            try:
                obj = CustomUser.objects.get(username=self.kwargs['username'])
                print(obj)
            except ObjectDoesNotExist:
                pass
        else:
            if self.request.user.is_authenticated:
                obj = self.request.user
            else:
                pass
        print(obj)
        # if obj is None:
        #     raise Http404()
        return obj


class UserPrivateProfilePageView(TemplateView):

    template_name = "users/private_profile_view.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CustomUserPrivateForm(initial={'username': request.user.username, 'email': request.user.email,'title': request.user.title,'bio_general': request.user.bio_general,'bio_research_interest': request.user.bio_research_interest, 'personal_website_address': request.user.personal_website_address, 'institution': request.user.institution})
            for key, value in form.fields.items():
                value.disabled = True
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('account_login'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CustomUserPrivateForm(request.POST)
            print(form.errors.as_data())

            if form.is_valid() :
                request.user.email = form["email"].value()
                request.user.title = form["title"].value()
                request.user.bio_general = form["bio_general"].value()
                request.user.bio_research_interest = form["bio_research_interest"].value()
                # request.user.connections = form["connections"].value()
                # request.user.institution = form["institution"].value()
                request.user.personal_website_address = form["personal_website_address"].value()
                request.user.institution = form["institution"].value()
                request.user.save()
                return redirect("userprofile_private_view")
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('account_login'))


class AcceptTermsPageView(TemplateView):

    template_name = "users/accept_terms_view.html"

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            latest_term = TermsPage.objects.latest('version_number')
            if request.user.accepted_eula_version == latest_term.version_number:
                return redirect("staticpages:homepage_view")
            else:
                return render(request, self.template_name, {'term_object': latest_term})
        else:
            return HttpResponseRedirect(reverse('account_login'))

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            acceptFlag = (request.POST.get("accept", "") == 'true');
            if acceptFlag:
                request.user.accepted_eula = True
                request.user.accepted_eula_version = request.POST.get("term-version", "")
                request.user.accepted_eula_date = date.today()
                request.user.save()
            else:
                logout(request)
            return redirect("staticpages:homepage_view")
        else:
            return HttpResponseRedirect(reverse('account_login'))
