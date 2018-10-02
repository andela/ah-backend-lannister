from rest_framework import serializers
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ('author','title','slug','description','body')