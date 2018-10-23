from rest_framework import serializers
from authors.apps.authentication.serializers import RegistrationSerializer,LoginSerializer
from authors.apps.authentication.models import User
   
class FbRegisterSerializer(RegistrationSerializer):
    def create(self, validated_data):
        
       user = User.objects.create_user(**validated_data)
       user.is_verified =True
       user.save()
       return user