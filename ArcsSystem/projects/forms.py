from django import forms

from projects.models import ProjectEntry, ProjectSubmission

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from django_summernote.fields import SummernoteTextFormField, SummernoteTextField


# code from: https://github.com/summernote/django-summernote/issues/391


import bleach

ALLOWED_TAGS = [
    'div', 'p', 'span', 'img', 'em', 'i', 'li', 'ol', 'ul', 'strong', 'br',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
#    'table', 'tbody', 'thead', 'tr', 'td',
    'img',
#    'abbr', 'acronym', 'b', 'blockquote', 'code', 'strike', 'u', 'sup', 'sub',
]

STYLES = [
    'background-color', 'font-size', 'line-height', 'color', 'font-family'
]

ATTRIBUTES = {
    '*': ['style', 'align', 'title', ],
    'img': ["src", ],
    'table': ['style', 'align', 'title', 'class',],


}

class HTMLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        return bleach.clean(
            value, tags=ALLOWED_TAGS, attributes=ATTRIBUTES, styles=STYLES)


# copy of code end here


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
        'science_type',
        'name',
        'aim',
        "image",
        'description',
        'status',
        'target_audience',
        'contact_name',
        "contact_email",
        'contact_role',
        'contact_affiliation',
        "description_card",
        "name_card",
        "aim_card",
        "url",


        ]


        widgets = {
        

        }

    aim =  HTMLField()
    description =  HTMLField()



    def __init__(self, *args, **kwargs):
        super(InitialProjectSubmissionModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            #self.fields[field].widget.attrs["class"] = "form-control col-2 col-sm-4 col-md-2"
            self.fields[field].widget.attrs["class"] = "form-control"








    #aim =  SummernoteTextFormField()
class ProjectEntryUpdateManagementForm(forms.ModelForm):
    """Form for maintaining the projects approved and added to the database.
    """
    model = ProjectEntry
    class Meta:
        model = ProjectEntry
        fields = [
        'science_type',
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

        ]
