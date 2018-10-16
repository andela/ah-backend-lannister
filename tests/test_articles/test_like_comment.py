from authors.apps.authentication.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests.test_authentication.test_base import BaseTest
from authors.apps.articles.models import Article


class CommentTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def create_second_user(self):
        user = User.objects.create_user('ckato','ckato@gmail.com','qww@1223wef')
        User.is_verified = True
        token = str(user.token(1))
        self.addcredentials(token)

    def create_an_article(self):
        user = User.objects.create_user(
            self.username, self.email, self.password)
        user.is_verified = True
        token = str(user.token(1))
        self.addcredentials(token)
        self.response = self.client.post(
            '/api/articles/', self.create_article, format="json")
        response = self.response.data
        return response['slug']

    def addcredentials(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token)

    def create_a_comment(self):
        slug = self.create_an_article()
        response = self.client.post(
            f'/api/articles/{slug}/comments/', self.test_comment, format="json")
        return response

    def test_like_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/like', format="json")   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_like_already_liked_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/like', format="json") 
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/like', format="json")  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_like_own_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/like', format="json")   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/like', format="json") 
        response = self.client.delete(
            f'/api/articles/{self.slug}/comments/{comment_id}/unlike', format="json")   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_comment_you_did_like(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        response = self.client.delete(
            f'/api/articles/{self.slug}/comments/{comment_id}/unlike', format="json")   
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)