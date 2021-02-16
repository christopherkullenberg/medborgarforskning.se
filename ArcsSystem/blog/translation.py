from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.decorators import register
from .models import  Post, Author, BlogPage

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration
class PostTranslationOptions(TranslationOptions):
    ''' Registers blog post fields for translation  '''
    fields = ('title', 'content')


translator.register(Post, PostTranslationOptions)

#class AuthorTranslationOptions(TranslationOptions):
#    fields = ('name')
#    ''' Registers blog author fields for translation '''

#translator.register(Author, AuthorTranslationOptions)

@register(BlogPage)
class BlogPageTranslationOptions(TranslationOptions):
    fields = (
        'body',
    )
