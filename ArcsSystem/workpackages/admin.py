from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from .models import WorkPackage, Theme

#class BlogAdmin(admin.ModelAdmin):
#    list_display = ('name', 'tagline')

class WorkPackageAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields = ("introduction", "detailed_content")
    fieldsets = [(u'WorkPackage', {'fields': ('name','introduction','detailed_content')})
        ]

class ThemeAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields = ('body',)

    fieldsets = [(u'Theme', {'fields': ('title','body', 'wp_parent','related_publications', 'keyword_lines', 'description')})
        ]



#admin.site.register(Blog, BlogAdmin)
admin.site.register(WorkPackage, WorkPackageAdmin)
admin.site.register(Theme,ThemeAdmin)
