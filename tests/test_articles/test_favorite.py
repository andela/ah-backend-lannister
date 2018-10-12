from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..test_authentication.test_base import BaseTest
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile

class FavoriteArticleTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.password = 'Ckato12345!'
        self.login_data = {"user": {
            "username": "ckato1",
            "email": "ckato1@gmail.com",
            "password": "Ckato12345!"
        }}
        self.login_data2 = {"user": {
            "username": "ckato2",
            "email": "ckato2@gmail.com",
            "password": "Ckato12345!"
        }}
        # create first user
        self.user1 = User.objects.create_user(
            'ckato1', 'ckato1@gmail.com', password=self.password)
        # activate account
        self.user1.is_active = True
        self.user1.is_verified = True
        self.user1.save()
        self.login_response1 = self.client.post(
            "/api/users/login/", self.login_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.article1 = self.client.post('/api/articles/',self.create_article, 
        format="json")
        self.assertEqual(self.article1.status_code, status.HTTP_201_CREATED)
        # create second user
        self.user2 = User.objects.create_user(
            'ckato2', 'ckato2@gmail.com', password=self.password)
        # activate account
        self.user2.is_active = True
        self.user2.is_verified = True
        self.user2.save()
        self.login_response2= self.client.post(
            "/api/users/login/", self.login_data2, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response2.data['token']
        )
        self.article2 = self.client.post('/api/articles/',self.create_article, 
        format="json")
        self.assertEqual(self.article2.status_code, status.HTTP_201_CREATED)

    def test_favorite_article(self):

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.response = self.client.post('/api/articles/{}/favorite/'.format(self.article2.data["slug"]))
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)    

    def test_favorite_favorited_article(self):
    
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.client.post('/api/articles/{}/favorite/'.format(self.article2.data["slug"]))
        self.response = self.client.post('/api/articles/{}/favorite/'.format(self.article2.data["slug"]))

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_favorite_own_article(self):
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.response = self.client.post('/api/articles/{}/favorite/'.format(self.article1.data["slug"]))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_non_slug_article(self):
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.response = self.client.post('/api/articles/{}/favorite/'.format('x-x-x'))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfavorite_article(self):
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.client.post('/api/articles/{}/favorite/'.format(self.article2.data["slug"]))
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format(self.article2.data["slug"]))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)    
    
    def test_unfavorite_unfavorited_article(self):
    
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.client.post('/api/articles/{}/favorite/'.format(self.article2.data["slug"]))
        self.client.delete('/api/articles/{}/unfavorite/'.format(self.article2.data["slug"]))
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format(self.article2.data["slug"]))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_unfavorite_unexistent_article(self):
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response1.data['token']
        )
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format('x-x-x'))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)  