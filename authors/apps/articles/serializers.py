from authors.apps.articles.models import Article, RateArticle, LikeArticle
from authors.apps.authentication.models import User
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""
    author = serializers.ReadOnlyField(source='author.username')
    read_time = serializers.ReadOnlyField(source='read')

    class Meta:
        model = Article
        """ List all of the fields that could possibly be included in a request
        or response, including fields specified explicitly above."""

        fields = ('author', 'title', 'slug', 'description',
                  'body', 'created_at', 'updated_at', 'read_time', 'average_rating', 'likes', 'dislikes')
        read_only_fields = ('slug', 'author_id',)


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
