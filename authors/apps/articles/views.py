import json
from authors.apps.articles.renderers import ArticleJSONRenderer
from authors.apps.articles.serializers import ArticleSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from .models import Article, RateArticle, LikeArticle
from .renderers import ArticleJSONRenderer, RateUserJSONRenderer, LikeUserJSONRenderer
from .serializers import ArticleSerializer, RateArticleSerializer, LikeArticleSerializer
from .models import Article, RateArticle
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from authors.apps.articles.renderers import ArticleJSONRenderer, TagJSONRenderer
from authors.apps.articles.serializers import ArticleSerializer, TagSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Article
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import TagHasNoArticles
from taggit.models import Tag 
from django.http import JsonResponse

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = (TagJSONRenderer,)
    serializer_class = TagSerializer


class TagRetrieveAPIView(generics.RetrieveAPIView):

    permission_classes = (AllowAny,)
    renderer_classes = (TagJSONRenderer,)
    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        tag_name = self.kwargs["tag_name"]
        tags = Article.objects.filter(tags__name__in=[tag_name]).values()
        if tags:
            return JsonResponse({'articles': list(tags)}, status=status.HTTP_200_OK)
        else:
            raise TagHasNoArticles("This tag currently has no articles")

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
        return Response({"message": "article deleted"}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        article_dict = request.data.get("article", {})
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied
        serializer = self.get_serializer(
            instance, data=article_dict, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RateArticleView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RateUserJSONRenderer,)
    queryset = RateArticle.objects.all()
    serializer_class = RateArticleSerializer

    def create(self, request, *args, **kwargs):
        article_slug = get_object_or_404(Article, slug=self.kwargs['slug'])
        get_rated_article = RateArticle.objects.filter(
            article_id=article_slug.id, rated_by_id=request.user.id)
        if article_slug.author_id == request.user.id:
            return Response({"msg": "you can not rate your own article"})
        if get_rated_article:
            return Response({"msg": "you have already rated this article"})
        rating = request.data.get('rate', {})
        serializer = self.serializer_class(data=rating)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, article_slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, article_slug):
        serializer.save(rated_by=self.request.user, article=article_slug)


class LikeArticleView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (LikeUserJSONRenderer,)
    queryset = LikeArticle.objects.all()
    serializer_class = LikeArticleSerializer

    def create(self, request, *args, **kwargs):
        article_slug = get_object_or_404(Article, slug=self.kwargs['slug'])
        instance = LikeArticle.objects.filter(
            article_id=article_slug.id, liked_by_id=request.user.id).first()
        if instance:
            return Response({"msg": "you can only like an article once"}, status=status.HTTP_400_BAD_REQUEST)

        liking = request.data.get('like', {})
        serializer = self.serializer_class(data=liking)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, article_slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, article_slug):
        serializer.save(liked_by=self.request.user, article=article_slug)


class LikeAPIDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """retreive, update and delete an article """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (LikeUserJSONRenderer,)
    serializer_class = LikeArticleSerializer
    queryset = LikeArticle.objects.all()

    def update(self, request, *args, **kwargs):
        article_slug = get_object_or_404(Article, slug=self.kwargs['slug'])
        liking = request.data.get("like", {})
        instance = LikeArticle.objects.filter(
            article_id=article_slug.id, liked_by_id=request.user.id).first()
        if not instance:
            raise PermissionDenied
        serializer = self.get_serializer(instance, data=liking)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RateArticleView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RateUserJSONRenderer,)
    queryset = RateArticle.objects.all()
    serializer_class = RateArticleSerializer

    def create(self, request, *args, **kwargs):
        article_slug = get_object_or_404(Article, slug=self.kwargs['slug'])
        get_rated_article = RateArticle.objects.filter(
            article_id=article_slug.id, rated_by_id=request.user.id)
        if article_slug.author_id == request.user.id:
            return Response({"msg": "you can not rate your own article"})
        if get_rated_article:
            return Response({"msg": "you have already rated this article"})
        rating = request.data.get('rate', {})
        serializer = self.serializer_class(data=rating)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, article_slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, article_slug):
        serializer.save(rated_by=self.request.user, article=article_slug)
