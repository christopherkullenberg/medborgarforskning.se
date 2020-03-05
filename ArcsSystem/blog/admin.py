from django.contrib import admin
from .models import Blog, Author, Entry

class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','email')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Author, AuthorAdmin)
# Register your models here.
