from modeltranslation.translator import translator, TranslationOptions
from .models import Article

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration
class PublicationTranslationOptions(TranslationOptions):
    pass
class ArticleTranslationOptions(TranslationOptions):
    ''' Registers blog post fields for translation  '''
    fields = ('title', 'abstract')

# order matters if you are loading a model depedning on another model
#translator.register(Publication, PublicationTranslationOptions)
translator.register(Article, ArticleTranslationOptions)
