from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .test_base import BaseTest

class RegistrationTests(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def test_valid_registration(self):
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.username, str(response.data))
        self.assertIn("Token", str(response.data))
        self.assertIn("link has been sent", str(response.data))

    def test_invalid_email(self):
        self.reg_data['user']['email'] = 'simon'
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid email", str(response.data))

    def test_invalid_password(self):
        self.reg_data['user']['password'] = '12'
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("8 characters", str(response.data))

    def test_password_not_alphanumeric(self):
        self.reg_data['user']['password'] = '12345678'
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("contain a letter and a number", str(response.data))

    def test_missing_email_field(self):
        del self.reg_data['user']['email']
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("is required", str(response.data))

    def test_invalid_username(self):
        self.reg_data['user']['username']='@#######'
        response = self.client.post("/api/users/",self.reg_data,format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid Username',str(response.data))
        
    def test_existing_email(self):
        self.client.post(
            '/api/users/', self.reg_data, format="json")
        response = self.client.post(
            '/api/users/', self.reg_data, format="json")
        self.assertIn("already exists", str(response.data))

