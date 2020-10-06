from django.contrib import admin
from .models import ProjectEntry, Keyword, ScienceType, ProjectSubmission




admin.site.register(ProjectEntry)
admin.site.register(Keyword)
admin.site.register(ScienceType)
admin.site.register(ProjectSubmission)


# Register your models here.
