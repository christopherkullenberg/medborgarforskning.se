from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page
# Register your models here.

class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    published = ('published',)


#admin.site.register(Blog, BlogAdmin)
admin.site.register(Page, PageAdmin)
