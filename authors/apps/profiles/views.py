from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer,ProfilesSerializers
from .exceptions import ProfileDoesNotExist
from rest_framework.exceptions import PermissionDenied,ValidationError
import jwt
from decouple import config, Csv



class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):

    """
    retrieve:
    fetch a user's profile
    update:
    Modify a user's profile.
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,) 
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        
        try:

            profile = Profile.objects.select_related('user').get(
                user__username=self.kwargs["username"])
        
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

            

        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
       

        username=self.kwargs["username"]
        if username == request.user.username:
            user_data = request.data.get('profile', {})
            
            serializer_data = {

                'username': user_data.get('username', request.user.username),
                'first_name': user_data.get('first_name', request.user.profile.first_name),
                'last_name': user_data.get('last_name', request.user.profile.last_name),
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image),
                'following': user_data.get('following', request.user.profile.following),
                'number_of_articles': user_data.get('number_of_articles', request.user.profile.number_of_articles),
            }

            serializer = self.serializer_class(
                request.user.profile, data=serializer_data, context={'request': request}, partial=True
            )
            serializer.is_valid(raise_exception=True)

            serializer.update(request.user.profile, serializer_data)
            try:

                serializer.update(request.user, serializer_data)
            except:
                return Response({"username already exists, please pick another one"}, status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        raise PermissionDenied("You don't have rights to modify this profile")

class RetriveProfilesView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,) 
    serializer_class = ProfilesSerializers

    def retrieve(self, request, *args, **kwargs):
        
        try:

            profiles = Profile.objects.all()
        
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

            

        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)