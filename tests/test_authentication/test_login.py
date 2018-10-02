from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from authors.apps.authentication.models import User

from .test_base import BaseTest
from .test_retrieve_update import UpdateUser


class LoginTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        

    def test_valid_login(self):
        """Tests users login with a valid email and password """
        User.objects.create_user(self.username,self.email,self.password)
        user = User.objects.get(email=self.email)
        user.is_active = True
        user.is_verified = True
        user.save()
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