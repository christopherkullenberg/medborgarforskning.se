from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.decorators import register
from .models import  (
                      TermsPage,
                      PressPage,)

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration

@register(TermsPage)
class TermsPageTranslationOptions(TranslationOptions):
    fields = (
        'terms_title',
        'terms_content'
    )

@register(PressPage)
class PressPageTranslationOptions(TranslationOptions):
    fields = (
    'press_title',
    'press_body'
    )
