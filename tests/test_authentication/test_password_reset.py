from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from authors.apps.authentication.models import User

from .test_base import BaseTest
from .test_retrieve_update import UpdateUser


class PasswordRestTestCase(APITestCase, BaseTest):
    """This class is a definition of tests for testing password reset using email"""

    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.email = 'kimbsimon@gmail.com'
        # Create a user
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def password_reset_request(self, email):
        # Test user email
        self.user_email = {
            'user': {
                'email': email
            }
        }
        self.response = self.client.post('/api/users/password_reset',
                                         data=self.user_email, format='json')
        return self.response

    def reset_password(self, password, email):
        # here get token from the email sent
        user = get_object_or_404(User, email=email)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(user.token(0.0208333)))
        self.response = self.client.put(
            '/api/users/password_reset/change/', self.user_password_reset_data, format='json')
        return self.response

    def test_initiating_password_reset(self):
        """Test if email is sent when user initiates password reset"""
        response = self.password_reset_request(self.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_initiating_password_reset_with_invalid_user(self):
        """Test unregistered email trying to reset password"""
        email = 'unknown@andela.com'
        response = self.password_reset_request(email)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sending_empty_email_for_reset(self):
        """ Test sending password reset request with empty email"""
        email = ''
        response = self.password_reset_request(email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resetting_password(self):
        """Test correct resetting of password"""
        response = self.reset_password(self.password, self.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorised_user_clicking_on_reset_link(self):
        response = self.client.put(
            '/api/users/password_reset/change/', self.user_password_reset_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_is_returned_when_email_is_clicked(self):
        user = get_object_or_404(User, email=self.email)
        token = str(user.token(0.0208333))
        response = self.client.get(
            f'/api/users/password_reset/confirm/{token}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_has_been_updated(self):
        response = self.reset_password(self.password, self.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset_with_to_email_field(self):
        self.response = self.client.post(
            '/api/users/password_reset', format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
    
