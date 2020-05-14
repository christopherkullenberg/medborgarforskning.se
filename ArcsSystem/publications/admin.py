from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Article, Keyword


class ArticleAdmin(TranslationAdmin):
    fieldsets = [
        (u'Article', {'fields': ('title','abstract')})
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword)
