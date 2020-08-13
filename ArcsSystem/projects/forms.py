from django import forms

from projects.models import ProjectEntry, ProjectSubmission

# Make sure to use: https://docs.djangoproject.com/en/2.2/ref/csrf/

class InitialProjectSubmissionModelForm(forms.ModelForm):
    """Creates the form to submit a project for approval for add to the
    database. This is different than the managment form which includes more
    fields and has a different workflow after a project is included in the
    database of projects.
    """
    model = ProjectSubmission
    class Meta:
        model = ProjectSubmission
        fields = [
        'aim',
        'name',
        'description',
        'status',
        'target_audience',
        'contact_name',
        'contact_role',
        'contact_affiliation',
        'keywords'
        ]

class ProjectEntryUpdateManagementForm(forms.ModelForm):
    """Form for maintaining the projects approved and added to the database.
    """
    model = ProjectEntry
    class Meta:
        model = ProjectEntry
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
