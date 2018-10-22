from rest_framework import status, serializers
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Profile, FollowingUser
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer,ProfilesSerializers, FollowerSerializer
from .exceptions import ProfileDoesNotExist
from rest_framework.exceptions import PermissionDenied, ValidationError
import jwt
from decouple import config, Csv
from authors.apps.authentication.models import User


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

        username = self.kwargs["username"]
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
        profiles = Profile.objects.all()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowView(CreateAPIView):
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = FollowerSerializer
    permission_classes = (IsAuthenticated,)

    model = FollowingUser
    queryset = FollowingUser.objects.all()

    def create(self, request, **kwargs):
        """ Add the current user to followers of the user passed in the URL as username 
            Param: username
        """
        profile = get_object_or_404(User, username=self.kwargs["username"])
        follower_profile = get_object_or_404(Profile, user=request.user)

        following_user = request.user.username
        followed_user = profile.username

        if profile.pk is follower_profile.pk:
            raise serializers.ValidationError('You cannot follow yourself')

        if not follower_profile.following:
            follower_profile.following = True
            follower_profile.save()

        data = {'following_user': request.user.id, 'followed_user': profile.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "{} you are now following {}".format(following_user,followed_user)})


class UnfollowView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    model = FollowingUser
    queryset = FollowingUser.objects.all()

    def delete(self, request, **kwargs):
        """ This method is used to make a user unfollow another user"""

        follower = request.user.id
        followed = get_object_or_404(User, username=self.kwargs["username"])

        try:
            following = FollowingUser.objects.get(
                followed_user_id=followed.id, following_user_id=follower)
            following.delete()

            return Response({"message": "you are no longer following {}".format(self.kwargs["username"])})

        except FollowingUser.DoesNotExist:
            return Response({"message": "you are not following {}".format(self.kwargs["username"])},status=status.HTTP_400_BAD_REQUEST)
