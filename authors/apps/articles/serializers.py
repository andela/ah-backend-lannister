from rest_framework import serializers
from authors.apps.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""
    author = serializers.ReadOnlyField(source='author.username')
   
    class Meta:
        model = Article
        """ List all of the fields that could possibly be included in a request
        or response, including fields specified explicitly above."""
        
        fields = ('author','title','slug','description','body','created_at','updated_at')
        read_only_fields = ('slug','author_id',)
