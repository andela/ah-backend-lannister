from decouple import config
from django.core.mail import EmailMessage
from django.utils.encoding import force_text
from rest_framework import serializers, status
from rest_framework.authentication import get_authorization_header
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect

from authors.apps.authentication.backends import JWTAuthentication
from authors.apps.authentication.models import User

from .renderers import UserJSONRenderer
from .send_email import send_gridmail
from .serializers import (LoginSerializer, PasswordResetSerializer,
                          RegistrationSerializer, UserSerializer)


class RegistrationAPIView(APIView):

    """
    post:
    Register a user to the platform.
    """
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        self.sendEmailVerification(user, request, user_data)
        return Response(user_data, status=status.HTTP_201_CREATED)

    def sendEmailVerification(self, user, request, user_data):
        username = user['username']
        subject = "Ah haven Account Verification"
        body = "Hello {}, Thank you for creating an account with us, kindly click on the link below to activate your account! \n\n \
                {}/api/users/verify_account/{}/" .format(username, request.get_host(), user_data['token'])
        to_email = [user["email"]]
        email = EmailMessage(subject, body, to=to_email,)
        email.send()
        user_data.update({
            'message': 'A verification link has been sent to your Email, please visit your Email and activate your account'
                    })
        
        
class LoginAPIView(APIView):

    """
    post:
    Login a registered user.
    """

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    retrieve:
    fetch a user's details.
    update:
    Modify a user's details.

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserAccountVerifyView(APIView, JWTAuthentication):
    """
    get user email:
    send verification link to the user email.

    """
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, token):
       
        try:
            user, user_token = self.authenticate_credentials(request, token)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('https://ah-frontend-lannister.herokuapp.com/login')

            raise serializers.ValidationError(
                'Activation link invalid or expired'
            )
        except:
            raise serializers.ValidationError(
                'Activation link invalid or expired'
            )


class UserPasswordReset(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # check data with serializer
        data_from_serializer = self.serializer_class(data=user)
        data_from_serializer.is_valid(raise_exception=True)

        # send email method
        email = data_from_serializer.data['email']
        token = data_from_serializer.data['token']
        host = 'http://'+request.get_host()+'/api/users/password_reset/confirm/'
        url = user.get('url', host)+token
        response = send_gridmail(email, url)
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, token, *args, **kwargs):
        url = request.get_host()
        #validate url here if its valid ie token
        # else send them invalid token message
        res = {'message': 'use this token to reset password',
               "token": token, 'url': 'http://'+url+'/api/users/password_reset/change/'}
        return Response(res, status=status.HTTP_200_OK)


class UpdatePassword(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        url = request.get_host()
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #blacklist the token here 
        res = {'message': 'password has been succefully reset,click the link to login',
               'url': 'http://'+url+'/api/users/login/'}
        return Response(res, status=status.HTTP_200_OK)
