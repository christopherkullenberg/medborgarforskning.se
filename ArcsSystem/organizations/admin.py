from django.contrib import admin
from .models import Organization
#from django_summernote.admin import SummernoteModelAdmin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Organization, OrganizationAdmin)
