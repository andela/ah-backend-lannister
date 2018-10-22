from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .serializers import NotificationSerializer, CommentNotificationSerializer
from .renderers import NotificationJSONRenderer
from .models import Notification, CommentNotification
from authors.apps.profiles.models import Profile
from .utils import merge_two_dicts


class NotificationDetailsView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = NotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):

        try:
            notification = Notification.objects.get(pk=pk)
            serializer = self.serializer_class(
                notification, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                'errors': 'Notification does not exist'
            }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):

        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'errors': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in notification.notified.all():
            notification.notified.remove(user.id)
            notification.save()
            message = "You have successfully deleted this notification"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response({
                'errors': 'You cannot delete this notification'
            }, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):

        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in notification.notified.all():
            notification.read.add(user.id)
            notification.save()
            message = "You have successfully marked the notification as read"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({
                'errors':
                'You cannot mark as read a notification that is not yours'
            }, status.HTTP_403_FORBIDDEN)


class NotificationAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = NotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        user = request.user
        notifications = Notification.objects.all()
        data = {}

        for notification in notifications:
            if user in notification.notified.all():
                serializer = self.serializer_class(
                    notification, context={'request': request})
                data[notification.id] = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):

        notifications = Notification.objects.all()
        user = request.user
        for notification in notifications:
            if user in notification.notified.all():
                notification.read.add(user.id)
                notification.save()
                message = "You successfully marked all notifications as read"
                response = {"message": message}
        return Response(response, status=status.HTTP_200_OK)


class AllNotificationsAPIView(APIView):

    notification_serializer_class = NotificationSerializer
    comment_serializer_class = CommentNotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        user = request.user
        article_notifications = Notification.objects.all()
        article_data = {}

        for notification in article_notifications:
            if user in notification.notified.all():
                serializer = self.notification_serializer_class(
                    notification, context={'request': request})
                article_data[notification.id] = serializer.data

        notifications = CommentNotification.objects.all()
        comment_data = {}

        for notification in notifications:
            if user in notification.notified.all():
                serializer = self.comment_serializer_class(
                    notification, context={'request': request})
                comment_data[notification.id] = serializer.data

        data = merge_two_dicts(article_data, comment_data)

        return Response(data, status=status.HTTP_200_OK)


class NotificationSwitchAppAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = NotificationSerializer

    def post(self, request):

        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.app_notification_enabled is True:
            profile.app_notification_enabled = False
            profile.save()
            message = "You have successfully deactivated in app notifications for articles"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        elif profile.app_notification_enabled is False:
            profile.app_notification_enabled = True
            profile.save()
            message = "You have successfully activated in app notifications for articles"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)


class NotificationSwitchEmailAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = NotificationSerializer

    def post(self, request):

        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.email_notification_enabled is True:
            profile.email_notification_enabled = False
            profile.save()
            message = "You have successfully deactivated email notifications"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        elif profile.email_notification_enabled is False:
            profile.email_notification_enabled = True
            profile.save()
            message = "You have successfully activated email notifications"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)


class CommentNotificationDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ Comment Notification View """

    serializer_class = CommentNotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):

        try:
            notification = CommentNotification.objects.get(pk=pk)
            serializer = self.serializer_class(
                notification, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                'errors': 'Notification does not exist'
            }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):

        try:
            notification = CommentNotification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'errors': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in notification.notified.all():
            notification.notified.remove(user.id)
            notification.save()
            message = "You have successfully deleted this notification"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response({
                'errors': 'You cannot delete this notification'
            }, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):

        try:
            notification = CommentNotification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in notification.notified.all():
            notification.read.add(user.id)
            notification.save()
            message = "You have successfully marked the notification as read"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({
                'errors':
                'You cannot mark as read a notification that is not yours'
            }, status.HTTP_403_FORBIDDEN)


class CommentNotificationAPIView(generics.RetrieveUpdateAPIView):

    serializer_class = CommentNotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):

        user = request.user
        notifications = CommentNotification.objects.all()
        data = {}

        for notification in notifications:
            if user in notification.notified.all():
                serializer = self.serializer_class(
                    notification, context={'request': request})
                data[notification.id] = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):

        notifications = CommentNotification.objects.all()
        user = request.user
        for notification in notifications:
            if user in notification.notified.all():
                notification.read.add(user.id)
                notification.save()
                message = "You successfully marked all notifications as read"
                response = {"message": message}
        return Response(response, status=status.HTTP_200_OK)


class CommentNotificationSwitchAppAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = CommentNotificationSerializer

    def post(self, request):

        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.app_notification_enabled is True:
            profile.app_notification_enabled = False
            profile.save()
            message = "You have successfully deactivated in app notifications for comments"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        elif profile.app_notification_enabled is False:
            profile.app_notification_enabled = True
            profile.save()
            message = "You have successfully activated in app notifications for comments"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)


class CommentNotificationSwitchEmailAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, )

    serializer_class = CommentNotificationSerializer

    def post(self, request):

        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.email_notification_enabled is True:
            profile.email_notification_enabled = False
            profile.save()
            message = "You have successfully deactivated email notifications for comments"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        elif profile.email_notification_enabled is False:
            profile.email_notification_enabled = True
            profile.save()
            message = "You have successfully activated email notifications for comments"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)
