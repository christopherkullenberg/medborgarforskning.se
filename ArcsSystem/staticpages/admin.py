from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Page, TermsPage, PressPage
# Register your models here.

class PageAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields = ('content',)
    fieldsets = [(u'Page', {'fields':('slug', 'category', 'published', 'title', 'content', 'sub_category')})
    ]

class TermsAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields = ('terms_content')
    fieldsets = [(u'TermsPage',{'fields': ('terms_title', 'terms_content', 'version_number')})
    ]

class PressAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields = ('press_body')
    filedsets = [(u'PressPage', {'fields':('press_title', 'pressPublishedDate', 'press_body', 'pressTags',)})
    ]

admin.site.register(Page, PageAdmin)
admin.site.register(TermsPage, TermsAdmin)
admin.site.register(PressPage, PressAdmin)
