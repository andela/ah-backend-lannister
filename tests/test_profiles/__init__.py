from django.test import TestCase
from rest_framework.test import APIClient


class BaseTest(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user_data = {"user": {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "Admin12345@"

        }

        }
        self.user_data1 = {"user": {
            "username": "ckato1",
            "email": "ckato1@gmail.com",
            "password": "Admin12345@"

        }
        }

        self.user_data2 = {"user": {
            "username": "ckato2",
            "email": "ckato2@gmail.com",
            "password": "Admin12345@"

        }
        }

        self.user_data3 = {"user": {
            "username": "ckato3",
            "email": "ckato3@gmail.com",
            "password": "Admin12345@"

        }
        }
        self.profile_data = {"profile": {
            "first_name": "muhumuza",
            "last_name": "brian",
            "email": "brian@gmail.com",
            "bio": "i am fab",
        }
        }

        self.profile_data_2 = {"profile": {
            "first_name": "chris",
            "last_name": " breezy",
            "email": "brian@gmail.com",
            "bio": "",
        }
        }

        self.profile_data_3 = {"profile": {
            "first_name": "spiderman",
            "email": "brian@gmail.com",
            "bio": "",
        }
        }
        self.profile_data_4 = {"profile": {
            "first_name": "spiderman",
            "email": "xyz@gmail.com",
            "bio": "",
        }
        }

        self.sign_up = self.client.post(
            "/api/users/", self.user_data, format="json")

        self.sign_up1 = self.client.post(
            "/api/users/", self.user_data1, format="json")
        self.sign_up2 = self.client.post(
            "/api/users/", self.user_data2, format="json")
        self.sign_up3 = self.client.post(
            "/api/users/", self.user_data3, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.sign_up1.data["token"])
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.sign_up.data["token"])
