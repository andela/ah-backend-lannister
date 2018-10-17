from django.urls import path
from .views import (
    NotificationDetailsView,
    NotificationAPIView,
    NotificationSwitchAppAPIView,
    NotificationSwitchEmailAPIView,
    CommentNotificationAPIView,
    CommentNotificationDetailsView,
    CommentNotificationSwitchAppAPIView,
    CommentNotificationSwitchEmailAPIView,
    AllNotificationsAPIView)


app_name = 'notifications'

urlpatterns = [
    # article notification urls
    path(
        'articles/<str:pk>',
        NotificationDetailsView.as_view(),
        name='notification'),
    path('articles', NotificationAPIView.as_view(), name='my_notifications'),
    path(
        'articles/switch_app/',
        NotificationSwitchAppAPIView.as_view(),
        name='switch_app_notifications'),
    path(
        'articles/switch_email/',
        NotificationSwitchEmailAPIView.as_view(),
        name='switch_email_notifications'),

    # comment notification urls
    path(
        'comments/<str:pk>',
        CommentNotificationDetailsView.as_view(),
        name='notification'),
    path(
        'comments',
        CommentNotificationAPIView.as_view(),
        name='my_notifications'),
    path(
        'comments/switch_app/',
        CommentNotificationSwitchAppAPIView.as_view(),
        name='switch_app_notifications'),
    path(
        'comments/switch_email/',
        CommentNotificationSwitchEmailAPIView.as_view(),
        name='switch_email_notifications'),

    path('all', AllNotificationsAPIView.as_view(), name='my_notifications'),



]
