from django import forms

# Make sure to use: https://docs.djangoproject.com/en/2.2/ref/csrf/

class ProjectSubmissionForm(forms.Form):
    """Creates the form to submit a project for approval for add to the
    database. This is different than the managment form which includes more
    fields and has a different workflow after a project is included in the
    database of projects.
    """
        pass

class ProjectManagementForm(forms.Form):
    """Form for maintaining the projects approved and added to the database.
    """
        pass
