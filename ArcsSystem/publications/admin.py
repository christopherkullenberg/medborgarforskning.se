from django.contrib import admin
from .models import Article, Keyword


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword)
