import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from taggit.models import Tag
from django.core.mail import EmailMessage

from .exceptions import CatHasNoArticles, TagHasNoArticles
from .models import (Article, Bookmark, Category, LikeArticle, RateArticle,
                     Reported)
from .renderers import (ArticleJSONRenderer, BookmarkJSONRenderer,
                        CategoryJSONRenderer, LikeUserJSONRenderer,
                        RateUserJSONRenderer, ReportArticleJSONRenderer,
                        ShareArticleJSONRenderer, TagJSONRenderer)
from .serializers import (ArticleSerializer, BookmarkSerializer,
                          CategorySerializer, LikeArticleSerializer,
                          RateArticleSerializer, ReportArticleSerializer,
                          ReportSerializer, ShareEmailSerializer,
                          TagSerializer)
from .utils import shareArticleMail
from rest_framework.views import APIView


class TagListAPIView(generics.ListAPIView):
    """ List all tags  """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = (TagJSONRenderer,)
    serializer_class = TagSerializer


class TagRetrieveAPIView(generics.RetrieveAPIView):
    """ Get articles under a specific tag """
    permission_classes = (AllowAny,)
    renderer_classes = (ArticleJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        tag_name = self.kwargs["tag_name"]
        tags = Article.objects.filter(tags__name__in=[tag_name]).values()
        if tags:
            return JsonResponse({'articles': list(tags)},
                                status=status.HTTP_200_OK)
        else:
            raise TagHasNoArticles("This tag currently has no articles")


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """ List / Create categories """

    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    renderer_classes = (CategoryJSONRenderer,)

    def create(self, request):
        category = Category.objects.filter(
            title=request.data.get('title'),
        )
        if category:
            raise ValidationError("Category with this title already exists")
        return super().create(request)


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    """ Get articles under a specific category """
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            cat_name = self.kwargs["cat_name"]
            category = Category.objects.get(title=cat_name)
            articles = Article.objects.filter(category=category).values()
            return Response({'articles': articles}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise CatHasNoArticles("The category currently has no articles")


class ArticleAPIView(generics.ListCreateAPIView):
    """create an article, list all articles paginated to 5 per page"""
    queryset = Article.objects.filter(is_published=True)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title', 'author__username', 'description', 'body', 'tags__name',)

    def create(self, request, *args, **kwargs):
        article = request.data.get("article", {})
        serializer = self.get_serializer(data=article)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__username=author)
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset


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
        return Response({"message": "article deleted"},
                        status=status.HTTP_200_OK)

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


class ArticleDraftAPIView(generics.ListAPIView):
    """create an article, list all draft articles paginated to 5 per page"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        auth_user = self.request.user
        queryset = Article.objects.filter(
            author_id=auth_user.id, is_published=False)
        return queryset
    
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        if queryset.count() == 0:
            return Response({"msg": "you have no articles"})
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        

class ArticlePublishedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        auth_user = self.request.user
        queryset = Article.objects.filter(
            author_id=auth_user.id, is_published=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        return ArticleDraftAPIView.list(self, request, *args, **kwargs)
       

class ArticleAPIPublishView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def update(self, request, *args, **kwargs):
        article = get_object_or_404(
                Article, slug=self.kwargs['slug'], author_id=request.user.id)
        
        if not article.is_published:
            article.is_published = True
            article.save()
            return Response(
                {"message": "article published succesfully"}, status=status.HTTP_201_CREATED)
        raise serializers.ValidationError(
            'article already published'
        )


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
            return Response({"msg": "you can only like an article once"},
                            status=status.HTTP_400_BAD_REQUEST)

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


class FavoriteArticleView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        profile = self.request.user.profile

        try:
            article = Article.objects.get(slug=self.kwargs['slug'])
            if article.author_id == profile.user_id:
                return Response(
                    {'error': 'You cannot favorite your own article'},
                    status=status.HTTP_400_BAD_REQUEST)
            if profile.has_favorited(article):
                return Response(
                    {'error': 'You already favorited this article'},
                    status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response(
                {'message': 'An article with this slug was not found.'},
                status=status.HTTP_404_NOT_FOUND)

        profile.favorite(article)
        article.favorites_count += 1
        article.save()

        serializer = self.serializer_class(article)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnFavoriteArticleView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def delete(self, request, *args, **kwargs):
        profile = self.request.user.profile

        try:
            article = Article.objects.get(slug=self.kwargs['slug'])
        except Article.DoesNotExist:
            return Response(
                {'message': 'An article with this slug was not found.'},
                status=status.HTTP_404_NOT_FOUND)
        if not profile.has_favorited(article):
            return Response(
                {'message': 'This article is not among your favorites'},
                status=status.HTTP_400_BAD_REQUEST)

        profile.unfavorite(article)
        if article.favorites_count > 0:
            article.favorites_count -= 1

        article.save()

        serializer = self.serializer_class(article)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ShareArticleAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ShareArticleJSONRenderer,)
    serializer_class = ShareEmailSerializer

    def create(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        article = get_object_or_404(Article, slug=article_slug)
        share = request.data.get('share', {})
        serializer = self.serializer_class(data=share)
        serializer.is_valid(raise_exception=True)
        share_data = serializer.data
        shareArticleMail(share, request, share_data, article)
        return Response(share_data, status=status.HTTP_200_OK)


class ReportArticle(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportArticleSerializer
    renderer_classes = (ReportArticleJSONRenderer,)
    lookup_field = "slug"
    queryset = Article.objects.all()

    def post(self, request, *args, **kwargs):
        report_data = request.data.get('report', {})
        article = get_object_or_404(Article, slug=kwargs['slug'])
        if article.author_id == request.user.id:
            raise PermissionDenied("you cant report your article")
        if Reported.objects.filter(article=article, user=request.user):
            raise PermissionDenied("you can only report once")
        serializer = self.serializer_class(data=report_data)
        serializer.is_valid(raise_exception=True)
        article.times_reported += 1
        article.save()
        serializer.save(article=article, user=request.user)
        msg = {'message': 'The article has been reported to the site admin'}
        return Response(msg, status=status.HTTP_201_CREATED)


class ReportArticleListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    renderer_classes = (ReportArticleJSONRenderer,)
    serializer_class = ReportArticleSerializer
    queryset = Reported.objects.all()


class ReportView(ReportArticleListView):
    queryset = Reported.objects.order_by('article_id').distinct('article_id')
    serializer_class = ReportSerializer


class BookmarkView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    renderer_classes = (BookmarkJSONRenderer,)
    queryset = Bookmark.objects.all()

    def create(self, request, *args, **kwargs):
        slug = get_object_or_404(Article, slug=self.kwargs['slug'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Bookmark.objects.filter(
            slug_id=slug.slug, user_id=request.user.id).first()
        if instance:
            return Response({"message": "you have already bookmarked this article"},
                            status=status.HTTP_200_OK)

        self.perform_create(serializer, slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, slug):
        serializer.save(user=self.request.user, slug=slug)


class UnBookmarkView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    lookup_field = 'slug'
    queryset = Bookmark.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = Bookmark.objects.filter(
            user_id=request.user.id, slug_id=self.kwargs['slug']).first()
        if not instance:
            return Response({"message": "bookmark not found"})
        self.perform_destroy(instance)
        return Response({"message": "deleted"},
                        status=status.HTTP_200_OK)


class AllBookmarksView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BookmarkJSONRenderer,)
    queryset = Bookmark.objects.all()

    def get(self, request, *args, **kwargs):
        bookmarks = self.queryset.filter(
            user_id=request.user)
        serializer = self.serializer_class(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
