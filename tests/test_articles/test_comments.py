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
        user = User.objects.create_user('kimbug','kimg@ff.com','qww@1223wef')
        User.is_verified = True
        token = str(user.token(1))
        self.addcredentials(token)

    def create_an_article(self):
        user = User.objects.create_user(
            self.username, self.email, self.password)
        User.is_verified = True
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

    def test_create_comment(self):
        response = self.create_a_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.delete(
            f'/api/articles/{self.slug}/comments/{comment_id}', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.put(
            f'/api/articles/{self.slug}/comments/{comment_id}', self.test_comment_edited, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.get(
            f'/api/articles/{self.slug}/comments/{comment_id}',format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_comment(self):
        comment = self.create_a_comment()
        response = self.client.get(
            f'/api/articles/{self.slug}/comments/',format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_when_not_owner(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        response = self.client.delete(
            f'/api/articles/{self.slug}/comments/{comment_id}', format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_when_not_owner(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.create_second_user()
        response = self.client.put(
            f'/api/articles/{self.slug}/comments/{comment_id}', self.test_comment_edited, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_thread(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.get(
            f'/api/articles/{self.slug}/comments/{comment_id}',format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_existing_comment(self):
        comment = self.create_a_comment()
        response = self.client.get(
            f'/api/articles/{self.slug}/comments/12',format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_reply_to_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/thread',self.test_comment,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_reply_to_comment(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.get(
            f'/api/articles/{self.slug}/comments/{comment_id}/thread',format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_comment_without_data(self):
        slug = self.create_an_article()
        response = self.client.post(
            f'/api/articles/{slug}/comments/', format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_comment_with_no_data(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.put(
            f'/api/articles/{self.slug}/comments/{comment_id}', format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_make_a_thread_with_no_data(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{comment_id}/thread',format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_edit_history(self):
        comment = self.create_a_comment()
        comment_id = comment.data['id']
        self.client.put(
            f'/api/articles/{self.slug}/comments/{comment_id}', self.test_comment_edited, format="json")
        response =self.client.get(
            f'/api/articles/{self.slug}/comments/{comment_id}/edit-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_edit_history(self):
        comment=self.create_a_comment()
        comment_id = comment.data['id']
        response =self.client.get(
            f'/api/articles/{self.slug}/comments/{comment_id}/edit-history/')
        self.assertIn("never been edited", str(response.data))
        


    

