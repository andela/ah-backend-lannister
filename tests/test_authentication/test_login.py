from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .test_base import BaseTest

class LoginTest(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()


    def test_valid_login(self):
        """Tests users login with a valid email and password """
        response = self.client.post(
            '/api/users/login/', self.userlogin , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.email,str(response.data))
        self.assertIn(self.username,str(response.data))
        self.assertIn("token",str(response.data))
        
    

    def test_no_email(self):
        """Tests users login with without an email supplied"""
        response = self.client.post(
            '/api/users/login/', self.no_email_login , format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("An email address is required to log in.",str(response.data))
    

    def test_no_password(self):
        """Tests users login with without password supplied"""
        response = self.client.post(
            '/api/users/login/', self.self_no_password_login , format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A password is required to log in.",str(response.data))
    


