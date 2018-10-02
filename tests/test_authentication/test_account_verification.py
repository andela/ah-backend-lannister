from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from authors.apps.authentication.models import User 
from .test_base import BaseTest

class AccountVerification(APITestCase,BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.response = self.client.post(
            '/api/users/', self.reg_data, format="json") 
    
    def test_send_email(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", str(self.response.data))
    
    def test_return_token(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", str(self.response.data))
    
    def test_verify_account(self):
        self.user=User.objects.create_user('simodfffd','kfddfssss@andela.com','weretgdfergf3')
        self.token = self.user.token()
        respond = self.client.get("/api/users/verify_account/{}/".format(self.token),
            format="json")
        user1 = User.objects.get(email='kfddfssss@andela.com')
        res = user1.is_verified
        self.assertTrue(res)
        self.assertIn("message", str(respond.data))
        self.assertEqual(status.HTTP_200_OK,respond.status_code)

    def test_failed_verify_account(self):
        self.user = User.objects.get(email=self.email)
        self.token = self.user.token
        self.client.get("/api/users/verify_account/{}/".format(self.token),
            format="json")
        response = self.client.get("/api/users/verify_account/{}/".format(self.token),
            format="json")
        self.assertIn("error", str(response.data))
        self.verify = self.user.is_verified
        self.assertFalse(self.verify)
    
    def test_no_login_for_unverified_user(self):
        """Test the api cannot login an unverified user."""
        self.user = User.objects.get(email=self.email)
        self.user.is_active = True
        self.user.is_verified = False
        self.user.save()
        self.response = self.client.post(
            "/api/users/login/",
            self.user_login,
            format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, self.response.status_code)

    def test_wrong_verification_link(self):
        self.user = User.objects.get(email=self.email)
        self.token = self.user.token
        self.response = self.client.get(
            "/api/users/verify_account/{}/".format(self.token),
            format="json")
        self.assertIn('Activation link invalid or expired', str(self.response.data))
