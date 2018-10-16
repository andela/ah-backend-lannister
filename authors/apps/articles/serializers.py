from authors.apps.articles.models import Article, RateArticle, LikeArticle, Category
from authors.apps.authentication.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
                                          
from taggit.models import Tag


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for articles."""
    author = serializers.ReadOnlyField(source='author.username')
    read_time = serializers.ReadOnlyField(source='read')
    tags = TagListSerializerField()
    
    class Meta:
        model = Article
        """ List all of the fields that could possibly be included in a request
        or response, including fields specified explicitly above."""

        fields = ('author', 'title', 'slug', 'description',
                  'body', 'created_at', 'updated_at', 'read_time', 'average_rating', 'likes', 'dislikes','tags','category','favorites_count')
        read_only_fields = ('slug', 'author_id',)

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('name',)

class CategorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = ('id','title','slug')
        read_only_fields = ('id', 'slug',)

        
class RateArticleSerializer(serializers.ModelSerializer):
    rated_by = serializers.ReadOnlyField(source='rated_by.username')
    article = serializers.ReadOnlyField(source='article.slug')

    class Meta:
        model = RateArticle
        fields = ['rated_by', 'date_created', 'rating', 'article']

    def validate(self, data):
        rating = data.get('rating')
        if not rating in range(1, 6):
            raise serializers.ValidationError(
                "Your rating should be in range of 1 to 5."
            )

        return {
            "rating": rating,

        }


class LikeArticleSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    article = serializers.ReadOnlyField(source='article.slug')

    class Meta:
        model = LikeArticle
        fields = ['liked_by', 'article', 'likes']

    def validate(self, data):
        likes = data.get('likes')
        if likes == None:
            raise serializers.ValidationError(
                {"likes": "This field is required"}
            )

        return {
            "likes": likes}


    def get_favorites_count(self, instance):
        return instance.favorited_by.count()
