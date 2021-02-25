from django.contrib import admin
from .models import ProjectEntry, KeywordSwe, KeywordEng, KeywordLine ,ScienceType, ProjectSubmission

admin.site.register(ProjectEntry)
admin.site.register(KeywordSwe)
admin.site.register(KeywordEng)
admin.site.register(KeywordLine)


admin.site.register(ScienceType)
admin.site.register(ProjectSubmission)


# Register your models here.
