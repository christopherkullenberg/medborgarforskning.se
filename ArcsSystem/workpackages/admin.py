from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import WorkPackage, Theme

#class BlogAdmin(admin.ModelAdmin):
#    list_display = ('name', 'tagline')

class WorkPackageAdmin(admin.ModelAdmin):
    summernote_fields = ("introduction", "detailed_content")

class ThemeAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)



#admin.site.register(Blog, BlogAdmin)
admin.site.register(WorkPackage, WorkPackageAdmin)
admin.site.register(Theme, ThemeAdmin)
