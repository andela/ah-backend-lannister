from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
# from tests.test_authentication.test_base import BaseTest
from ..test_authentication.test_base import BaseTest
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from django.urls import reverse

class ArticleTagsTest(APITestCase,BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def create_login_user(self):
        user=User.objects.create_user(self.username,self.email,self.password)
        User.is_verified=True
        token=str(user.token(1))
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        self.addcredentials(token)

    def addcredentials(self,response):
        self.client.credentials(
        HTTP_AUTHORIZATION='Token ' + response)

    def test_create_article(self):
        self.create_login_user()
        response = self.client.post('/api/articles/',self.create_article, 
        format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)      
    
    def test_create_article_with_tag(self):

        """
        Tests the creation of an article with a single tag. 
        """
        self.create_login_user()
        response = self.client.post(
                '/api/articles/',
                self.create_article,
                format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(['r', 'e', 'a', 'c', 't', 'j', 's'], response.data['tags'][0])

    def test_create_article_with_tags(self):
        """
        Tests creation of an article with several tags. 
        """
        self.create_login_user()
        response = self.client.post('/api/articles/',
                                    self.create_article_several_tags,
                                    format="json",        
                                    )
        slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': slug})
        response = self.client.get(self.retrieve_update_delete_url,
                                   format="json")
        self.assertTrue(len(response.data['tags']) > 1)

    def test_create_article_with_tags_already_in_database(self):
        """
        Tests that a user can create several articles with the same tags.
        """
        self.create_login_user()
        self.client.post('/api/articles/',
                         self.create_article,
                         format="json",
                         )
        response = self.client.post('/api/articles/',
                                    self.create_article_several_tags,
                                    format="json",
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
