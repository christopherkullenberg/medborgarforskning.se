from modeltranslation.translator import translator, TranslationOptions
from .models import WorkPackage, Theme

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration
#class WorkPackageTranslationOptions(TranslationOptions):
#    pass
class WorkPackageTranslationOptions(TranslationOptions):
    ''' Registers Work Oackage post fields for translation  '''
    fields = ('name', 'introduction', 'detailed_content')

class ThemeTranslationOptions(TranslationOptions):
    ''' Registers theme post fields for translation  '''
    fields = ('title', 'body')
# order matters if you are loading a model depedning on another model
translator.register(WorkPackage, WorkPackageTranslationOptions)
translator.register(Theme, ThemeTranslationOptions)
