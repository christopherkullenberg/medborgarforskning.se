from django import forms

from projects.models import Project

# Make sure to use: https://docs.djangoproject.com/en/2.2/ref/csrf/

class InitialProjectSubmissionModelForm(forms.ModelForm):
    """Creates the form to submit a project for approval for add to the
    database. This is different than the managment form which includes more
    fields and has a different workflow after a project is included in the
    database of projects.
    """
    model = Project
    class Meta:
        model = Project
        fields = [
        'aim',
        'name',
        'description',
        'start_date',
        'end_date',
        'status',
        'target_audience',
        'contact_name',
        'contact_role',
        'contact_affiliation',
        'contact_email',
        'contact_phone',
        'keywords'
        ]


class ProjectManagementForm(forms.ModelForm):
    """Form for maintaining the projects approved and added to the database.
    """
    pass
