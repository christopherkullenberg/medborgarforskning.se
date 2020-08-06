from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.decorators import register
from .models import  HomePage

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration

@register(HomePage)
class BlogPageTranslationOptions(TranslationOptions):
    fields = (
        'welcome_body',
        'project_body',
        'get_CitSciSE_box',
        'data_box',
        'paper_box',
        'CitSciSE_box',
    )
