from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from authors.apps.articles.renderers import ArticleJSONRenderer
from authors.apps.articles.serializers import ArticleSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Article
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class ArticleAPIView(generics.ListCreateAPIView):
    """create an article, list all articles paginated to 5 per page"""
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        article = request.data.get("article", {})
        serializer = self.get_serializer(data=article)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   


class ArticleAPIDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """retreive, update and delete an article """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    queryset = Article.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(instance)
        return Response({"message":"article deleted"},status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        article_dict = request.data.get("article", {})
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied
        serializer = self.get_serializer(instance, data=article_dict, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
