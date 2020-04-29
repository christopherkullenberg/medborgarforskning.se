from django.contrib import admin
from .models import Product, Article, Arcsreport, Keyword


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)

#admin.site.register(Product, ProductAdmin)
#admin.site.register(Article)
#admin.site.register(Arcsreport)
#admin.site.register(Keyword)


# Register your models here.
