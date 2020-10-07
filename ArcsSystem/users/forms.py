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

class CustomUserPrivateForm(UserChangeForm):
    # institution = forms.CharField(widget=forms.Select(choices=CHOICES))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'title', 'bio_general', 'bio_research_interest', 'personal_website_address', "first_name", "last_name")

    def __init__(self, *args, **kwargs):

        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.SlugField(
            required=False,
            widget=forms.TextInput(attrs={'readonly':'readonly'})
        )
        organizations = Organization.objects.all()
        choices = (("", "Select"),)
        for org in organizations:
            choices = choices + ((org.name,org.name),)
        self.fields['institution'] = forms.CharField(widget=forms.Select(choices=choices))

# class CustomUserPrivateForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=200)
#     bio_general = forms.CharField(label="Short Intro Biography", max_length=500)
#     bio_research_interest = forms.CharField(label="Short Outline of your Interests", max_length=500)
#     connections = forms.CharField(label="Describe the connections and/or collaboration you are seeking.", max_length=400)
#     institution = forms.CharField(label="Institution", max_length=200)

#     def __init__(self, *args, **kwargs):
#         super(CustomUserPrivateForm, self).__init__()
#         # print(kwargs)
#         # print(kwargs['initial'].title)
#         # print(kwargs['initial'].bio_general)
#         # print(kwargs['initial'].bio_research_interest)
#         # print(kwargs['initial'].connections)
#         # print(kwargs['initial'].institution)
