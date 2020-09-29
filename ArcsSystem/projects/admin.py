from django.contrib import admin
from .models import (ProjectEntry,
                    Keyword,
                    ScienceType)

admin.site.register(ProjectEntry)
admin.site.register(Keyword)
admin.site.register(ScienceType)
# Register your models here.
