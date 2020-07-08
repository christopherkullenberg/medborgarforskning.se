from django.utils import translation
from django.test import Client, TestCase
from .models import Keyword, Project
from django.urls import reverse
from django.conf import settings

### May want to break this test file up by test focus ie test_models.py, test_forms.py, test_views.py it becomes very large.)

# test_models.py
# Create your tests here.


# Create your tests here.


class ProjectTestCare(TestCase):
    """docstring for PublicationTestCare."""

    def setUp(self):
        self.keyword1 = Keyword.objects.create(
            keyword = 'AI'
            )
        self.keyword2 = Keyword.objects.create(
            keyword = 'deep learning'
            )
        self.keyword3 = Keyword.objects.create(
            keyword = 'Machine learning'
            )

        self.project = Project.objects.create(
            aim = 'Just for test.',
            description = 'This is a test project.',
            name = 'test',
            start_date = '2019-07-07',
            end_date = '2019-07-08',
            status = '2',
            target_audience = 'Project primary audience.',
            contact_name = 'aram',
            contact_role = 'developer',
            contact_affiliation = 'coworker',
            contact_email = 'aram@test.com',
            contact_phone = '+46765525418'
            )

        self.project.keywords.add(self.keyword1)
        self.project.keywords.add(self.keyword2)
        self.project.keywords.add(self.keyword3)

        self.project.save()

        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]


    # test_forms.py
    # Create your tests here.


    # test_views.py
    # Create your tests here.
    def test_projects_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.project.get_absolute_url())
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(self.project.get_absolute_url())
            self.assertEqual(no_response.status_code, 404)


    def test_projects_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.project.get_absolute_url_details())
                no_response = self.client.get('projects/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(self.project.get_absolute_url_details())
            self.assertEqual(no_response.status_code, 404)


    def test_project_search_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('projects:search_results'), { 'q': 'AI'})
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('projects:search_results'), { 'q': 'AI'})
            self.assertEqual(no_response.status_code, 404)


    def test_project_submission_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('projects:project_submissionform'))
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('projects:project_submissionform'))
            self.assertEqual(no_response.status_code, 404)


    def test_projects_query(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.project.get_absolute_url())
                self.assertQuerysetEqual(response.context['project_list'], ['<Project: test>'])
                response_details = self.client.get(self.project.get_absolute_url_details())
                self.assertContains(response_details, 'This is a test project.')
                response_search = self.client.get(reverse('projects:search_results'), { 'q': 'AI'})
                self.assertQuerysetEqual(response_search.context['project_list'], ['<Project: test>'])


    def test_projects_display_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response_list = self.client.get(self.project.get_absolute_url())
                response_detail = self.client.get(self.project.get_absolute_url_details())
                response_search = self.client.get(reverse('projects:search_results'), { 'q': 'AI'})
                response_sunmissionform = self.client.get(reverse('projects:project_submissionform'))
                self.assertEqual(response_list.resolver_match.func.__name__, 'ProjectListView')
                self.assertEqual(response_detail.resolver_match.func.__name__, 'ProjectDetailView')
                self.assertEqual(response_search.resolver_match.func.__name__, 'SearchResultsView')
                self.assertEqual(response_sunmissionform.resolver_match.func.__name__, 'ProjectSubmissionCreateView')
