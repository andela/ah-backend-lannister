from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
# from tests.test_authentication.test_base import BaseTest
from ..test_authentication.test_base import BaseTest
from authors.apps.articles.models import Article, Category
from authors.apps.authentication.models import User

class ArticlesTest(APITestCase,BaseTest):
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
    
    def test_no_user_auth_create(self):
        response = self.client.post('/api/articles/',self.create_article, 
        format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_article(self):
        self.create_login_user()
        article = self.client.post('/api/articles/',self.create_article, 
        format="json")
        articleslug = article.data["slug"]
        response = self.client.put('/api/articles/{}/'.format(articleslug), 
        self.update_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_wrong_update_article(self):
        self.create_login_user()
        article = self.client.post('/api/articles/',self.create_article, 
        format="json")
        articleslug = article.data["slug"]
        response = self.client.put('/api/articles/{}/'.format(articleslug), 
        self.wrong_article_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_view_article(self):
        self.create_login_user()
        article = self.client.post('/api/articles/',self.create_article, 
        format="json")
        articleslug = article.data["slug"]
        response = self.client.get('/api/articles/{}/'.format(articleslug), 
        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_article(self):
        self.create_login_user()
        article = self.client.post('/api/articles/',self.create_article, 
        format="json")
        articleslug = article.data["slug"]
        response = self.client.delete('/api/articles/{}/'.format(articleslug), 
        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_no_auth_user_delete(self):
        articleslug = "x-x-x"
        response = self.client.delete('/api/articles/{}/'.format(articleslug), 
        format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_no_user_auth_update(self):
        articleslug = "x-x-x"
        response = self.client.put('/api/articles/{}/'.format(articleslug), 
        self.wrong_article_update,
         format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





        

    