from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.models import User
from tests.test_authentication.test_base import BaseTest
from rest_framework import status
from authors.apps.notifications.utils import merge_two_dicts


class Base(APITestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

    def create_login_user(self):
        user = User.objects.create_user(
            self.username, self.email, self.password)
        User.is_verified = True
        token = str(user.token(1))
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        self.addcredentials(token)

    def addcredentials(self, response):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response)

    def test_retrieve_notifications(self):
        """ Test a user can retrieve all notifications """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.get(
            "/api/notifications/all", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_comment_notifications(self):
        """ Test a user can retrieve all comment notifications """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.get(
            "/api/notifications/comments", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_notification(self):
        """ Test a user can retrieve a single notification """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        notification = self.client.get(
            "/api/notifications/articles", format="json")
        pk = [*notification.data][0]
        response = self.client.get(
            "/api/notifications/articles", kwargs={'pk': pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_notification_doesnot_exist(self):
        """ Test a user can retrieve a comment notification that doesn't exist """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.get(
            f"/api/notifications/comments/{500}", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Notification does not exist", str(response.data))

    def test_get_article_notification_doesnot_exist(self):
        """ Test a user can retrieve an article notification that doesn't exist """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.get(
            f"/api/notifications/articles/{500}", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_notification_doesnot_exist(self):
        """ Test a user can delete a comment notification that doesnot exist """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.delete(
            f"/api/notifications/comments/{500}", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article_notification_doesnot_exist(self):
        """ Test a user can delete an article notification that doesnot exist """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.delete(
            f"/api/notifications/articles/{500}", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_as_read_article_notification_doesnot_exist(self):
        """ Test a user can mark as read an article notification that doesn't exist """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.put(
            f"/api/notifications/articles/500", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_as_read_comment_notification_doesnot_exist(self):
        """ Test a user can mark as read a comment  notification that doesn't exist """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.put(
            f"/api/notifications/comments/500", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successfully_delete_notification(self):
        """
        Tests that a user can delete a notification.
        """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        notification = self.client.get(
            "/api/notifications/comments", format="json")
        pk = [*notification.data][0]
        response = self.client.get(
            f"/api/notifications/comments/{pk}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_notification(self):
        """ Test a user can delete comment notification """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/comments", format="json")
        pk = [*notification.data][0]
        response = self.client.delete(
            f"/api/notifications/comments/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_notification_when_not_owner(self):
        """ Test delete comment notification when not owner """
        self.set_up_comment_notifications()

        email = 'user2@user2.com'
        password = '12345678'
        user = {
            "user": {
                "email": email,
                "password":password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/comments", format="json")
        pk = [*notification.data][0]
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.delete(
            f"/api/notifications/comments/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article_notification_when_not_owner(self):
        """ Test delete article notification when not owner """
        self.set_up_notifications()

        email = 'user2@user2.com'
        password = '12345678'
        user = {
            "user": {
                "email": email,
                "password":password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/articles", format="json")
        pk = [*notification.data][0]
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.delete(
            f"/api/notifications/articles/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_mark_article_notification_as_read_when_not_owner(self):
        """ Test mark article notification as read when not owner """
        self.set_up_notifications()

        email = 'user2@user2.com'
        password = '12345678'
        user = {
            "user": {
                "email": email,
                "password":password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/articles", format="json")
        pk = [*notification.data][0]
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.put(
            f"/api/notifications/articles/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_comment_notification_as_read_when_not_owner(self):
        """ Test mark comment notification as read when not owner """
        self.set_up_comment_notifications()

        email = 'user2@user2.com'
        password = '12345678'
        user = {
            "user": {
                "email": email,
                "password":password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/comments", format="json")
        pk = [*notification.data][0]
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user_login, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        response = self.client.put(
            f"/api/notifications/comments/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_article_notification(self):
        """ Test a user can delete article notification """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)
        notification = self.client.get(
            "/api/notifications/articles", format="json")
        pk = [*notification.data][0]
        response = self.client.delete(
            f"/api/notifications/articles/{pk}", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_deactivate_article_app_notification(self):
        """
        Tests that a can user successfully deactivate in app article notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        self.client.post(
            "/api/notifications/articles/switch_app/", format="json")
        response = self.client.post(
            "/api/notifications/articles/switch_app/", format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_successfully_activate_article_app_notification(self):
        """
        Tests that a user can successfully activate in app article notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/articles/switch_app/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    def test_successfully_deactivate_articles_email_notification(self):
        """
        Tests that a user can successfully deactivate article email notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/articles/switch_email/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have successfully deactivated email notifications", str(response.data))


    def test_successfully_activate_articles_email_notification(self):
        """
        Tests that a user can successfully activate articles email notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/articles/switch_email/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have successfully deactivated email notifications", str(response.data))

    def test_successfully_mark_article_notification_as_read(self):
        """
        Tests that a user can mark all article notifications as read.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.put(
            "/api/notifications/articles", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You successfully marked all notifications as read" , str(response.data))


    def test_successfully_mark_comment_notifications_as_read(self):
        """
        Tests that a user can mark all comment notifications as read.
        """
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.put(
            "/api/notifications/comments", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You successfully marked all notifications as read" , str(response.data))

    def test_successfully_mark_single_comment_notification_as_read(self):
        """ Test a user can mark a single comment_notification as read"""
        self.set_up_comment_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        notification = self.client.get(
            "/api/notifications/comments", format="json")
        pk = [*notification.data][0]
        response = self.client.put(
            "/api/notifications/comments", kwargs={'pk': pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You successfully marked all notifications as read" , str(response.data))

    def test_successfully_mark_single_article_notification_as_read(self):
        """ Test a user can mark a single article notification as read"""
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        notification = self.client.get(
            "/api/notifications/articles", format="json")
        pk = [*notification.data][0]
        response = self.client.put(
            "/api/notifications/articles", kwargs={'pk': pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_successfully_deactivate_comment_app_notification(self):
        """
        Tests that a user can successfully deactivate in app comment notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/comments/switch_app/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have successfully deactivated in app notifications for comments",
        str(response.data))
        

    def test_successfully_activate_comment_app_notification(self):
        """
        Tests that a user can successfully activate in app comment notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/comments/switch_app/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have successfully deactivated in app notifications for comments",
        str(response.data))


    def test_successfully_deactivate_comment_email_notification(self):
        """
        Tests that a user can successfully deactivate comment email notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/comments/switch_email/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have successfully deactivated email notifications for comments",
        str(response.data))

    def test_successfully_activate_comment_email_notification(self):
        """
        Tests that a user successfully activate comment email notifications.
        """
        self.set_up_notifications()

        self.email = 'user2@user2.com'
        self.password = '12345678'
        self.user = {
            "user": {
                "email": self.email,
                "password": self.password
            }
        }
        self.loginresponse = self.client.post(
            "/api/users/login/", self.user, format="json")
        token = self.loginresponse.data['token']
        self.addcredentials(token)

        response = self.client.post(
            "/api/notifications/comments/switch_email/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("'You have successfully deactivated email notifications for comments",
        str(response.data))


    def test_merge_two_dicts(self):

        dict1 = {'a': 1, 'b': 2}
        dict2 = {'c': 3, 'd': 4}
        self.assertEqual(merge_two_dicts(dict1, dict2), {
                         'a': 1, 'b': 2, 'c': 3, 'd': 4})

    def set_up_notifications(self):
        # create user 1
        user = User.objects.create_user(
            self.username, self.email, self.password)
        user.is_verified = True
        user1token = user.token(1)
        user.save()
        # create user 2
        # login him in
        self.username = 'user223'
        self.email = 'user2@user2.com'
        self.password = '12345678'
        user = User.objects.create_user(
            self.username, self.email, self.password)
        user.is_verified = True
        user.save()

        token = user.token(1)
        self.addcredentials(token)
        # make him user 2 follow user 1

        self.client.post('/api/profiles/{}/follow/'.format('simon'))

        # login user 1 and make him post an article
        self.addcredentials(user1token)
        self.client.post('/api/articles/', self.create_article, format="json")

    def set_up_comment_notifications(self):
        # create user one
        user = User.objects.create_user(
            self.username, self.email, self.password)
        user.is_verified = True
        user1token = user.token(1)
        user.save()
        # create user two
        self.username = 'user223'
        self.email = 'user2@user2.com'
        self.password = '12345678'
        user = User.objects.create_user(
            self.username, self.email, self.password)
        user.is_verified = True
        user.save()

        token = user.token(1)

        # log user one in
        # make user one create an article
        self.addcredentials(user1token)

        self.client.post('/api/articles/', self.create_article, format="json")
        # log in user two
        # make user two favorite an article of user one
        self.addcredentials(token)
        self.client.post(
            '/api/articles/how-to-tnnrain-your-flywwwwwwwwwwf/favorite/',
            format="json")
        # log in user one
        # make him comment on his article
        self.addcredentials(user1token)
        self.client.post(
            '/api/articles/how-to-tnnrain-your-flywwwwwwwwwwf/comments/',
            self.test_comment,
            format="json")
