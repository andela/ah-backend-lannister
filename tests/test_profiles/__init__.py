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

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.sign_up.data["token"])

