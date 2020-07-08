from django.test import Client, TestCase
from .models import WorkPackage, Theme
from django.utils import translation
from django.urls import reverse
from django.conf import settings

# Create your tests here.

class WorkPackageTestCare(TestCase):

    def setUp(self):
        self.workpackage = WorkPackage.objects.create(
            name = 'Test',
            introduction = 'This is a Test for workpackages',
            detailed_content = 'content of workpackages'
            )

        self.theme = Theme.objects.create(
            title = 'ethics',
            body = 'test for body',
            related_papers_tags = ['workpackage', 'resource'],
            wp_parent = self.workpackage
            )

        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]

    # test_views.py
    # Create your tests here.

    def test_workpackage_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('workpackages:workpackages_list'))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'workpackages/workpackages_list.html')
        with translation.override('pr'):
            no_response = self.client.get(reverse('workpackages:workpackages_list'))
            self.assertEqual(no_response.status_code, 404)


    def test_workpackages_display_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response_list = self.client.get(reverse('workpackages:workpackages_list'))
                response_detail = self.client.get(self.workpackage.get_absolute_url(), kwargs={'category' : self.workpackage.name})
                response_theme = self.client.get(reverse('workpackages:theme_view', kwargs={'category' : self.workpackage.name, 'title' : self.theme.title}))
                self.assertEqual(response_list.resolver_match.func.__name__, 'WorkpackagesListView')
                self.assertEqual(response_detail.resolver_match.func.__name__, 'WorkpackagesCategoryView')
                self.assertEqual(response_theme.resolver_match.func.__name__, 'WorkpackagesDetailView')



    # def test_workpackage_details_view(self):
    #     for each_language in self.languages_list:
    #         with translation.override(each_language):
    #             response = self.client.get(reverse('workpackages:theme_view', kwargs={'category' : self.workpackage.name, 'title' : self.theme.title}))
    #             no_response = self.client.get('resources/12345')
    #             self.assertEqual(no_response.status_code, 404)
    #             self.assertEqual(response.status_code, 200)
    #             self.assertTemplateUsed(response, 'workpackages/theme_view.html')
    #     with translation.override('pr'):
    #         no_response = self.client.get(reverse('workpackages:theme_view',
    #             kwargs={'category' : self.workpackage.name, 'title' : self.theme.title}))
    #         self.assertEqual(no_response.status_code, 404)

    # def test_workpackage_category_view(self):
    #     for each_language in self.languages_list:
    #         with translation.override(each_language):
    #             print("#############" + self.workpackage.get_absolute_url())
    #             response = self.client.get(self.workpackage.get_absolute_url())
    #             no_response = self.client.get('resources/12345')
    #             self.assertEqual(no_response.status_code, 404)
    #             self.assertEqual(response.status_code, 200)
    #             self.assertTemplateUsed(response, 'workpackages/category_view.html')
    #     with translation.override('pr'):
    #         no_response = self.client.get(self.workpackage.get_absolute_url())
    #         self.assertEqual(no_response.status_code, 404)
