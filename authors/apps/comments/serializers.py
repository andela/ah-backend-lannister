from django.shortcuts import get_object_or_404
from rest_framework import serializers

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField('get_is_parent')
    author = serializers.SerializerMethodField()
    parent = serializers.ReadOnlyField(source='authors.parent')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'author', 'replies',
                  'created_at', 'updated_at', 'parent')

    def get_is_parent(self, obj):
        if not obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return obj.parent

    def get_author(self, obj):
        x = get_object_or_404(Profile, user=obj.author)
        return ProfileSerializer(x).data

    def validate(self, data):
        return CommentChildSerializer.validate(self, data)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image', 'following')


class CommentChildSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'author', 'created_at', 'updated_at', 'parent')

    def validate(self, data):
        body = data.get('body', None)
        if body is None:
            raise serializers.ValidationError(
                'Please insert the body of the comment'
            )
        return data
