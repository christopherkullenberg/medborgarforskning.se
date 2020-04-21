from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Author, Post

#class BlogAdmin(admin.ModelAdmin):
#    list_display = ('name', 'tagline')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','email')

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    published = ('published',)


#admin.site.register(Blog, BlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
# Register your models here.
