from rest_framework import status

from tests.test_profiles import BaseTest
from authors.apps.profiles.models import Profile 


class UserProfile(BaseTest):
    """This class tests activities concerning user model"""

    def test_get_user_profile(self):
        """"This method tests setting up a new profile"""
        response = self.client.get("/api/profiles/admin/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "first_name" in response.data

    def test_update_user_profile(self):
        """"This method tests updating a user profile with data"""
        response = self.client.put("/api/profiles/admin/", self.profile_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.profile_data['profile']['first_name'],response.data['first_name'])
        self.assertIn(self.profile_data['profile']['bio'],response.data['bio'])

    def test_update_user_profile_empty_field(self):
        """"This method tests updating a field on user profile with no data"""
        response = self.client.put("/api/profiles/admin/", self.profile_data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_missing_attribute(self):
        """"This method tests updating a user profile with a missing attribute"""
        response = self.client.put("/api/profiles/admin/", self.profile_data_3, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_new_email(self):
        """"This method tests updating a user profile with a missing attribute"""
        response = self.client.put("/api/profiles/admin/", self.profile_data_4, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    

    



    

    

    