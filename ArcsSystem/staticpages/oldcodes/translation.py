from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.decorators import register
from .models import  (HomePage,
                      TermsPage,
                      PrivacyPage,
                      SourcecodePage,
                      PressPage,
                      CitizenSciencePage,
                      # WhatIsCitizenSciencePage,
                      SwedishCitizenSciencePage,
                      CaseStudiesPage,
                      FAQPage,
                      AdditionalResourcesPage,
                      WhatsCitizenSciencePage)

# Supported fields - https://django-modeltranslation.readthedocs.io/en/latest/registration.html#supported-fields-matrix

# One class per model defining which Model and Fields are registerd for translation via django-modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/registration.html#registration

@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = (
        'welcome_body',
        'project_body',
        'get_CitSciSE_box',
        'data_box',
        'paper_box',
        'CitSciSE_box',
    )

@register(TermsPage)
class TermsPageTranslationOptions(TranslationOptions):
    fields = (
        'terms_title',
        'terms_content'
    )

@register(PrivacyPage)
class PrivacyPageTranslationOptions(TranslationOptions):
    fields = (
        'privacy_title',
        'privacy_content'
    )

@register(SourcecodePage)
class SourcecodePageTranslationOptions(TranslationOptions):
    fields = (
    'sourcecode_title',
    'sourcecode_content'
    )

@register(PressPage)
class PressPageTranslationOptions(TranslationOptions):
    fields = (
    'press_title',
    'press_body'
    )

@register(CitizenSciencePage)
class CitizenScienceTranslationOptions(TranslationOptions):
    fields = (
        'citizen_science_menu_title',
    )


# @register(WhatIsCitizenSciencePage)
# class WhatIsCitizenSciencePageTranslationOptions(TranslationOptions):
#     fields = (
#         'what_citizen_science_body',
#     )

@register(SwedishCitizenSciencePage)
class SwedishCitizenScienceTranslationOptions(TranslationOptions):
    fields = (
        'swedish_citizen_science_body',
    )

@register(CaseStudiesPage)
class CaseStudiesPageTranslationOptions(TranslationOptions):
    fields = (
        'case_studies_body',
    )

@register(FAQPage)
class FAQPageTranslationOptions(TranslationOptions):
    fields = (
        'faq_body',
    )

@register(AdditionalResourcesPage)
class AditionalResourcesPageTranslationOptions(TranslationOptions):
    fields = (
        'additional_resources_body',
    )

@register(WhatsCitizenSciencePage)
class WhatisCitizenSciencePageTranslationOptions(TranslationOptions):
    fields = (
    'citizen_science_body',
    )
