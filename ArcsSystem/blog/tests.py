from django.test import Client, TestCase
from django.utils import translation
from .models import Post, Author
from django.urls import reverse
from django.conf import settings
import datetime


class BlogTestCare(TestCase):
    """docstring for BlogTestCare."""

    def setUp(self):
        self.post = Post.objects.create(
            slug = 'FisrtBlog',
            title = 'blog test case',
            published = datetime.date(2020, 7, 13),
            content = 'test for blog pages',
            tags = ['test', 'blog'],
        )

        self.author = Author.objects.create(
            name = 'Aram Karimi',
            email = 'aram.test@test.com'
        )

        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]

    # test_forms.py
    # Create your tests here.


    # test_views.py
    # Create your tests here.

    def test_blog_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('blog:blog_list_view'))
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('blog:blog_list_view'))
            self.assertEqual(no_response.status_code, 404)


    def test_blog_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.post.get_absolute_url())
                no_response = self.client.get('blog/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(self.post.get_absolute_url())
            self.assertEqual(no_response.status_code, 404)


    def test_blog_post_month_archive_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('blog:archive_month_numeric', kwargs={'year' : self.post.published.year,
                                                                                'month' : self.post.published.month}))
                no_response = self.client.get('blog/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('blog:archive_month_numeric', kwargs={'year' : self.post.published.year,
                                                                                'month' : self.post.published.month}))
            self.assertEqual(no_response.status_code, 404)


    def test_blog_post_year_archive_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('blog:archive_year_numeric', kwargs={'year' : self.post.published.year}))
                no_response = self.client.get('blog/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('blog:archive_year_numeric', kwargs={'year' : self.post.published.year}))
            self.assertEqual(no_response.status_code, 404)


    def test_blog_post_days_archive_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('blog:archive_day_numeric', kwargs={'year' : self.post.published.year,
                                                                             'month' : self.post.published.month,
                                                                             'day' : self.post.published.day
                                                                             }))
                no_response = self.client.get('blog/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('blog:archive_day_numeric', kwargs={'year' : self.post.published.year,
                                                                         'month' : self.post.published.month,
                                                                         'day' : self.post.published.day
                                                                        }))
            self.assertEqual(no_response.status_code, 404)


    def test_blog_display_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response_list = self.client.get(reverse('blog:blog_list_view'))

                response_detail = self.client.get(self.post.get_absolute_url())

                response_archive_year = self.client.get(reverse('blog:archive_year_numeric', kwargs={'year' : self.post.published.year}))

                response_archive_month = self.client.get(reverse('blog:archive_month_numeric', kwargs={'year' : self.post.published.year,
                                                                                                'month' : self.post.published.month}))

                response_archive_day = self.client.get(reverse('blog:archive_day_numeric', kwargs={'year' : self.post.published.year,
                                                                                            'month' : self.post.published.month,
                                                                                            'day' : self.post.published.day
                                                                                            }))
                self.assertEqual(response_list.resolver_match.func.__name__, 'BlogPostIndexView')
                self.assertEqual(response_detail.resolver_match.func.__name__, 'BlogPostDateDetailView')
                self.assertEqual(response_archive_year.resolver_match.func.__name__, 'BlogPostYearArchiveView')
                self.assertEqual(response_archive_month.resolver_match.func.__name__, 'BlogPostMonthArchiveView')
                self.assertEqual(response_archive_day.resolver_match.func.__name__, 'BlogPostDayArchiveView')
