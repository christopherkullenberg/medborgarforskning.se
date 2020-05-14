from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Article, Keyword


class ArticleAdmin(TabbedTranslationAdmin):
    fieldsets = [
        (u'Article', {'fields': ('title','abstract')})
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword)
