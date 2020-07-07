from django.utils import translation
from django.test import Client, TestCase
from .models import Organization
from django.urls import reverse
from django.conf import settings
from django.test.utils import setup_test_environment

### May want to break this test file up by test focus ie test_models.py, test_forms.py, test_views.py it becomes very large.)

# test_models.py
# Create your tests here.
class OrganizationTestCare(TestCase):


    def setUp(self):
        self.organization = Organization.objects.create(
            name = 'University of Gothenburg',
            wikidataID = 'Q371522',
            description = 'The University of Gothenburg is a university in Swedens second largest city, Gothenburg.',
            website = 'www.gu.se'
        )
        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]

    def test_organization_listing(self):
        self.assertEqual(f'{self.organization.name}', 'University of Gothenburg')
        self.assertEqual(f'{self.organization.wikidataID}', 'Q371522')
        self.assertEqual(f'{self.organization.description}', 'The University of Gothenburg is a university in Swedens second largest city, Gothenburg.')
        self.assertEqual(f'{self.organization.website}', 'www.gu.se')


    def test_datbase_values(self):
        # Organization.objects.filter(name='University of Gothenburg').all()
        org = Organization.objects.get(wikidataID='Q371522')
        self.assertEqual(f'{org.name}', 'University of Gothenburg')
        self.assertEqual(f'{org.wikidataID}', 'Q371522')
        self.assertEqual(f'{org.description}', 'The University of Gothenburg is a university in Swedens second largest city, Gothenburg.')
        self.assertEqual(f'{org.website}', 'www.gu.se')

    # test_forms.py
    # Create your tests here.

    # test_views.py
    # Create your tests here.

    def test_organization_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('organizations:organization_list'))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'University of Gothenburg')
                self.assertTemplateUsed(response, 'organizations/organization_list.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('organizations:organization_list'))
            self.assertEqual(no_response.status_code, 404)


    def test_organization_details_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.organization.get_absolute_url())
                no_response = self.client.get('org/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'University of Gothenburg')
                self.assertTemplateUsed(response, 'organizations/organization_detail.html')
        with translation.override('pr'):
            no_response = self.client.get(self.organization.get_absolute_url())
            self.assertEqual(no_response.status_code, 404)


    def test_organizations_query(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('organizations:organization_list'))
                self.assertEqual(response.status_code, 200)
                self.assertQuerysetEqual(response.context['organization_list'], ['<Organization: University of Gothenburg>'])
