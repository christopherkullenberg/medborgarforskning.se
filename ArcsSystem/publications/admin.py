from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Article, Keyword


class ArticleAdmin(TabbedTranslationAdmin):
    fieldsets = [
        (u'Article', {'fields': ('title','abstract','keywords','doi','py','authors','source','volume','issue')})
    ]
    list_display = [
        'title',
        'abstract',
        'doi',
        'py',
        'authors',
        'source',
        'volume',
        'issue'
        ]
    search_fields = [
        'keywords',
        'title',
        'abstract',
        'doi',
        'py',
        'authors',
        'source'
        ]
    readonly_fields = [
        'title',
        'abstract',
        'doi',
        'py',
        'authors',
        'source',
        'volume',
        'issue'
    ]
    list_filter = [
        #'py',
        'source',
        ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword)
