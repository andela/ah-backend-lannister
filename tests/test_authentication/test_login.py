from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .test_base import BaseTest


class LoginTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.client.post(
            '/api/users/', self.reg_data, format="json")

    def test_valid_login(self):
        """Tests users login with a valid email and password """
        response = self.client.post(
            '/api/users/login/', self.user_login, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.email, str(response.data))
        self.assertIn("token", str(response.data))

    def test_no_password(self):
        self.user_login['user']['password'] = " "
        response = self.client.post(
            '/api/users/login/', self.user_login, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("blank", str(response.data))

    def test_no_email(self):
        self.user_login['user']['email'] = " "
        response = self.client.post(
            '/api/users/login/', self.user_login, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("blank", str(response.data))

    def test_user_does_not_exist(self):
        self.user_login['user']['email'] = "miriam@gmail.com"
        response = self.client.post(
            '/api/users/login/', self.user_login, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("wrong password or email", str(response.data))
