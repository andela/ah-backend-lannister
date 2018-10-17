from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

from ..test_authentication.test_base import BaseTest


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

    def addcredentials(self, response):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response)

    def test_bookmarking(self):
        self.create_login_user()
        response = self.client.post(
            f'/api/articles/{self.slug}/bookmark/', format="json")
        self.assertEqual(response.status_code, 201)

    def test_bookmarking_article_twice(self):
        self.create_login_user()
        self.client.post(
            f'/api/articles/{self.slug}/bookmark/', format="json")
        response = self.client.post(
            f'/api/articles/{self.slug}/bookmark/', format="json")
        self.assertIn("already bookmarked this article", str(response.data))

    def test_unbookmarking(self):
        self.create_login_user()
        self.client.post(
            f'/api/articles/{self.slug}/bookmark/', format="json")
        response = self.client.delete(
            f'/api/articles/{self.slug}/unbookmark/', format="json")
        self.assertIn("deleted", str(response.data))

    def test_get_all_bookmarks(self):
        self.create_login_user()
        response = self.client.get(
            f'/api/bookmarks/', format="json")
        self.assertEqual(response.status_code, 200)

    def test_ubookmarking_none_existing_bookmark(self):
        self.create_login_user()
        response = self.client.delete(
            f'/api/articles/{self.slug}/unbookmark/', format="json")
        self.assertIn("bookmark not found", str(response.data))
