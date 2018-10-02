from rest_framework import status
from django.utils.encoding import force_text
from authors.apps.authentication.models import User
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from django.core.mail import EmailMessage
from decouple import config

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
                {}/api/users/verify_account/{}/" .format(username,request.get_host(), user_data['token'])
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
    
class UserAccountVerifyView(APIView,JWTAuthentication):
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
                user.is_verified=True
                user.save()
                return Response({
                    'message': 'Your Account has been verified, continue to login',
                    }, status=status.HTTP_200_OK)

            raise serializers.ValidationError(
                'Activation link invalid or expired'
            )
        except:
            raise serializers.ValidationError(
                'Activation link invalid or expired'
            )