from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
import requests
from rest_framework import status
from authors.apps.authentication.models import User

from rest_framework.response import Response
from rest_auth.social_serializers import TwitterLoginSerializer
from authors.apps.authentication.serializers import RegistrationSerializer,LoginSerializer
from .serializers import FbRegisterSerializer
import json
from authors.apps.authentication.renderers import UserJSONRenderer

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    FbRegSerializer_class=FbRegisterSerializer
    renderer_classes = (UserJSONRenderer,)
    
    def post(self, request):
        data=request.data
        token=data['access_token']
        url = "https://graph.facebook.com/v3.1/me"

        querystring = {"fields":"id,name,email,first_name,last_name","access_token":token}
        response = requests.request("GET", url,params=querystring)
        i=json.loads(response.text)

        data={
                "password": 'Ah123456789@',
                "username": i.get('name'),
                "email": i.get('email'),
                }
        if not User.objects.filter(email=i.get('email')).exists():
            
            serializer=self.FbRegSerializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        loginserializer=LoginSerializer(data=data)
        loginserializer.is_valid(raise_exception=True)
        return Response(loginserializer.data)


        
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter