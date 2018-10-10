from rest_framework import serializers
from .models import Profile, FollowingUser

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)


    class Meta:
        model = Profile
        fields = ('username', 'first_name','last_name','bio','image','following','number_of_articles','created_at','updated_at')
        read_only_fields = ('username',)

class ProfilesSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    following = serializers.BooleanField()
    
    class Meta:
        model = Profile
        fields = ('username', 'first_name','last_name','bio', 'following','image')

class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowingUser
        fields = ('following_user','followed_user','date_added')

