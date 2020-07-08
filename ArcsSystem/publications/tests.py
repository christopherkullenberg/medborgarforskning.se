from django.test import Client, TestCase
from django.utils import translation
from .models import Article as artciles
from .models import Keyword
from django.urls import reverse
from django.conf import settings

# Create your tests here.


class PublicationTestCare(TestCase):
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

        self.Article = artciles.objects.create(
                title = 'Pre-training of Deep Bidirectional Transformers for Language Understanding',
                abstract = 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.',
                doi = '10.18653/v1/n19-1423',
                py = '750',
                authors = 'Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina ',
                source = 'https://www.bibsonomy.org/bibtex/210c860e3f390c6fbfd78a3b91ab9b0af/albinzehe',
                volume = '2-8',
                issue = 'issue'
            )

        self.Article.keywords.add(self.keyword1)
        self.Article.keywords.add(self.keyword2)
        self.Article.keywords.add(self.keyword3)

        self.Article.save()

        self.client = Client()
        self.languages_list = [language_code[0] for language_code in settings.LANGUAGES]


    def test_publications_list_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('publications:article_publications_list'))
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('publications:article_publications_list'))
            self.assertEqual(no_response.status_code, 404)


    def test_publications_detail_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(self.Article.get_absolute_url())
                no_response = self.client.get('publications/12345')
                self.assertEqual(no_response.status_code, 404)
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(self.Article.get_absolute_url())
            self.assertEqual(no_response.status_code, 404)


    def test_publication_search_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('publications:search_publications_results'), { 'q': 'AI'})
                self.assertEqual(response.status_code, 200)
        with translation.override('pr'):
            no_response = self.client.get(reverse('publications:search_publications_results'), { 'q': 'AI'})
            self.assertEqual(no_response.status_code, 404)


    def test_publications_query(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response = self.client.get(reverse('publications:article_publications_list'))
                self.assertQuerysetEqual(response.context['article_list'], ['<Article: Pre-training of Deep Bidirectional Transformers for Language Understanding>'])
                response_details = self.client.get(self.Article.get_absolute_url())
                self.assertContains(response_details, 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.')
                response_search = self.client.get(reverse('publications:search_publications_results'), { 'q': 'AI'})
                self.assertQuerysetEqual(response_search.context['article_list'], ['<Article: Pre-training of Deep Bidirectional Transformers for Language Understanding>'])


    def test_publications_display_view(self):
        for each_language in self.languages_list:
            with translation.override(each_language):
                response_list = self.client.get(reverse('publications:article_publications_list'))
                response_detail = self.client.get(self.Article.get_absolute_url())
                response_search = self.client.get(reverse('publications:search_publications_results'), { 'q': 'AI'})
                self.assertEqual(response_list.resolver_match.func.__name__, 'ArticleListView')
                self.assertEqual(response_detail.resolver_match.func.__name__, 'ArticleDetailView')
                self.assertEqual(response_search.resolver_match.func.__name__, 'SearchPublicationsView')
