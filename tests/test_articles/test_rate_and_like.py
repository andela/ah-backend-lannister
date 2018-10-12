from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..test_authentication.test_base import BaseTest
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class ArticlesTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def create_login_user(self):
        user = User.objects.create_user(
            self.username, self.email, self.password)
        User.is_verified = True
        token = str(user.token(1))
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        self.addcredentials(token)
        self.client.post('/api/articles/', self.create_article, format="json")

    def create_login_user2(self):
        user = User.objects.create_user('mim', 'mim@gmail.com', 'Mim123@ghjo')
        User.is_verified = True
        token = str(user.token(1))
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        self.addcredentials(token)

    def addcredentials(self, response):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response)

    def test_valid_rating(self):
        self.create_login_user()
        self.create_login_user2()
        response = self.client.post(
            f'/api/articles/{self.slug}/rating/', self.rate_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_rating_own_article(self):
        self.create_login_user()
        response = self.client.post(
            f'/api/articles/{self.slug}/rating/', self.rate_data, format="json")
        self.assertIn("can not rate your own article", str(response.data))

    def test_invalid_rating(self):
        self.create_login_user()
        self.create_login_user2()
        self.rate_data['rate']['rating'] = 9
        response = self.client.post(
            f'/api/articles/{self.slug}/rating/', self.rate_data, format="json")
        self.assertIn("range of 1 to 5.", str(response.data))

    def test_rate_article_twice(self):
        self.create_login_user()
        self.create_login_user2()
        self.client.post(
            f'/api/articles/{self.slug}/rating/', self.rate_data, format="json")
        response = self.client.post(
            f'/api/articles/{self.slug}/rating/', self.rate_data, format="json")
        self.assertIn("already rated this article", str(response.data))
