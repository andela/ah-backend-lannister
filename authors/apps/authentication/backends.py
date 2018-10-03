import jwt

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from .models import User
from authors.settings import defaults

"""Configure JWT Here"""


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # split the authorization header into 2 to separate the Token prefix from the token
        auth = get_authorization_header(request).split()
        if not auth:
            return None
        if len(auth) == 1 or len(auth) > 2:
            return None
        if auth[0].lower().decode('utf-8') != 'token':
            return None

        return self.authenticate_credentials(request, auth[1])

    def authenticate_credentials(self, request, token):
        # decode the token to get the user with the provided cretentials
        try:
            decoded_token = jwt.decode(token, defaults.SECRET_KEY)
            user = User.objects.get(email=decoded_token['email'])
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed(
                "Token expired please Login again to get new token")
        except jwt.InvalidTokenError or jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token")

        return user, token
