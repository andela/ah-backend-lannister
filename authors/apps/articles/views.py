from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authors.apps.articles.renderers import ArticleJSONRenderer
from authors.apps.articles.serializers import ArticleSerializer

# Create your views here.
class ArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer


    def post(self, request):
        """
        creates an article
        :param request:
        :return:
        """
        article = request.data.get("article", {})
        article.update({"author": request.user.id})
        serializer = self.serializer_class(data=article,partial=True)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


