from django.utils import translation
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from .models import Page
from taggit.managers import TaggableManager

### May want to break this test file up by test focus ie test_models.py, test_forms.py, test_views.py it becomes very large.)

class ResourceTestCare(TestCase):
    """docstring for ResourceTestCare."""

    def setUp(self):
        self.page = Page.objects.create(
            slug = 'Arcs Project',
            category = 'Science',
            title = 'ARenas for Cooperation through citizen Science',
            published = '2020-06-30',
            content = 'A Swedish national hub for everyone interested in citizen science (medborgarforskning).',
            tags = ['collaboration', 'Sweden'],
        )

        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]

    # test_models.py
    # Create your tests here.


    # test_forms.py
    # Create your tests here.


    # test_views.py
    # Create your tests here.

    def test_staticpages_home_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:homepage_view'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'home.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:homepage_view'))
            self.assertEqual(no_response.status_code, 404)


    def test_staticpages_terms_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:terms_detail'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'staticpages/terms-cookies-privacy_detail.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:terms_detail'))
            self.assertEqual(no_response.status_code, 404)

    def test_staticpages_privacy_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:privacy_detail'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'staticpages/terms-cookies-privacy_detail.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:privacy_detail'))
            self.assertEqual(no_response.status_code, 404)

    def test_staticpages_sourcecode_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:sourcecode_detail'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'staticpages/terms-cookies-privacy_detail.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:sourcecode_detail'))
            self.assertEqual(no_response.status_code, 404)


    def test_staticpages_press_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:press_detail'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'staticpages/terms-cookies-privacy_detail.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:press_detail'))
            self.assertEqual(no_response.status_code, 404)


    def test_staticpages_category_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('staticpages:homepage_view'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'home.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('staticpages:homepage_view'))
            self.assertEqual(no_response.status_code, 404)


    def test_staticpages_display_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response_list = self.client.get(reverse('staticpages:homepage_view'))
                response_detail = self.client.get(reverse('staticpages:terms_detail'))
                self.assertEqual(response_list.resolver_match.func.__name__, 'HomePageView')
                self.assertEqual(response_detail.resolver_match.func.__name__, 'TermsPageView')
