from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile, FollowingUser


class UserFollowing(TestCase):
    """This class tests different scenarios for user following another user or author"""

    def setUp(self):
        self.client = APIClient()
        self.password = 'Ckato12345!'
        self.login_data = {"user": {
            "username": "ckato1",
            "email": "ckato1@gmail.com",
            "password": "Ckato12345!"
        }}

        # create first user
        self.user1 = User.objects.create_user(
            'ckato1', 'ckato1@gmail.com', password=self.password)
        # activate account
        self.user1.is_active = True
        self.user1.is_verified = True
        self.user1.save()
        self.login_response = self.client.post(
            "/api/users/login/", self.login_data, format='json')

        # create second user
        self.user2 = User.objects.create_user(
            'ckato2', 'ckato2@gmail.com', password=self.password)
        # activate account
        self.user2.is_active = True
        self.user2.is_verified = True
        self.user2.save()

    def test_follow_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token']
        )
        self.response = self.client.post('/api/profiles/{}/follow/'.format(self.user2.username))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_follow_self(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token']
        )
        self.response = self.client.post('/api/profiles/{}/follow/'.format(self.user1.username))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token']
        )
        self.client.post('/api/profiles/{}/follow/'.format(self.user2.username))
        self.response = self.client.delete('/api/profiles/{}/unfollow/'.format(self.user2.username))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_not_followed(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token']
        )
        self.response = self.client.delete('/api/profiles/{}/unfollow/'.format(self.user2.username))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


