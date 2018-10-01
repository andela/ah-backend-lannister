from rest_framework import status
from rest_framework.test import APIClient, APITestCase


from .test_base import BaseTest


class UpdateUser(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def create_login_user(self):
        self.client.post('/api/users/', self.reg_data, format="json")
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        self.addcredentials(self.loginresponse.data['token'])

    def addcredentials(self,response):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response)

    def test_user_retrieve_with_valid_token(self):
        self.create_login_user()
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', str(response.data))

    def test_user_update(self):
        self.create_login_user()
        response = self.client.put(
            "/api/user/", self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_without_token(self):
        response = self.client.post(
            "/api/user/", self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_without_token(self):
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_with_no_token(self):
        self.addcredentials(response='')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_wrong_token_prefix(self):
        self.client.credentials(HTTP_AUTHORIZATION='fdfd '+'dff')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_rieve_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+'dff')
        response = self.client.get("/api/user/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
