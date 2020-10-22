# users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from organizations.models import Organization

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class ViewProfile(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'title', 'bio_general', 'bio_research_interest', 'personal_website_address', "first_name", "last_name")

    def __init__(self, *args, **kwargs):

        super(ViewProfile, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.SlugField(
            required=False,
            widget=forms.TextInput(attrs={'readonly':'readonly'})
        )
        organizations = Organization.objects.all()
        choices = (("", "Select"),)
        for org in organizations:
            choices = choices + ((org.name,org.name),)
        self.fields['institution'] = forms.CharField(widget=forms.Select(choices=choices))

class EditProfileForm(forms.ModelForm):

    class Meta():
        model = get_user_model()
        fields = ( 'email', 'title', 'bio_general', 'bio_research_interest', 'personal_website_address', "first_name", "last_name")

    def __init__(self, *args, **kwargs):

        super(EditProfileForm, self).__init__(*args, **kwargs)
        organizations = Organization.objects.all()
        choices = (("", "Select"),)
        for org in organizations:
            choices = choices + ((org.name,org.name),)
        self.fields['institution'] = forms.CharField(widget=forms.Select(choices=choices))
