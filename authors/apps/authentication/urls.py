from django.urls import path

from .views import (LoginAPIView, RegistrationAPIView, UpdatePassword,
                    UserAccountVerifyView, UserPasswordReset,
                    UserRetrieveUpdateAPIView)

app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/verify_account/<token>/',
         UserAccountVerifyView.as_view(), name='verify_account'),
    path('users/password_reset', UserPasswordReset.as_view()),
    path('users/password_reset/confirm/<str:token>/',
         UserPasswordReset.as_view()),
    path('users/password_reset/change/', UpdatePassword.as_view()),

]
