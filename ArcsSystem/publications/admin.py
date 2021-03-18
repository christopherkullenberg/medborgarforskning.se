from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from .models import Article, Keyword


class ArticleAdmin(TabbedTranslationAdmin):
    fieldsets = [
        (u'Article', {'fields': ('title','abstract','keywords','doi','py','authors','source','volume','issue',)})
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword)
