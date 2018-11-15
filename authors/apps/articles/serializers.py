from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authors.apps.articles.models import (Article, Category, LikeArticle,
                                          RateArticle, Reported, Bookmark)
from authors.apps.authentication.models import User
from taggit.models import Tag
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for articles."""
    author = serializers.ReadOnlyField(source='author.username')
    category_title = serializers.ReadOnlyField(source='category.title')
    read_time = serializers.ReadOnlyField(source='read')
    tags = TagListSerializerField()
    is_published = serializers.ReadOnlyField()

    class Meta:
        model = Article
        """ List all of the fields that could possibly be included in a request
        or response, including fields specified explicitly above."""

        fields = (
            'author', 'title', 'slug', 'description', 'body', 'created_at', 
            'updated_at', 'read_time', 'average_rating', 'likes', 'dislikes', 
            'tags', 'category', 'favorites_count', 'image', 'published_on',
            'is_published', 'category_title')
        read_only_fields = ('slug', 'author_id', 'is_published')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')
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


class ShareEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def check(self, data):
        email = data.get['email', None]

        if email is None:
            raise serializers.ValidationError(
                'An email is required to share.'
            )


class ReportArticleSerializer(serializers.ModelSerializer):
    article_title = serializers.ReadOnlyField(source='article.title')
    article_slug = serializers.ReadOnlyField(source='article.slug')
    article_author = serializers.ReadOnlyField(source='article.author.email')
    reported_by = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Reported
        fields = ['article_title', 'reason', 'article_slug',
                  'article_author', 'reported_by']


class ReportSerializer(ReportArticleSerializer):
    times_reported = serializers.ReadOnlyField(source='article.times_reported')

    class Meta:
        model = Reported
        fields = ['article_title', 'article_slug',
                  'article_author', 'times_reported', 'reason']


class BookmarkSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='slug.author.username')
    slug = serializers.ReadOnlyField(source='slug.slug')
    image = serializers.ReadOnlyField(source='slug.image')
    article_title = serializers.ReadOnlyField(source='slug.title')
    description = serializers.ReadOnlyField(source='slug.title')

    class Meta:
        model = Bookmark
        fields = ['author', 'article_title', 'slug',
                  'description', 'bookmarked_at', 'image']
