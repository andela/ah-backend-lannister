from django.shortcuts import get_object_or_404, render
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from authors.apps.articles.models import Article

from .models import Comment
from .renderer import (CommentJSONRenderer, CommentsJSONRenderer,
                       CommentThreadJSONRenderer)
from .serializers import CommentChildSerializer, CommentSerializer


# Create your views here.
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentsJSONRenderer,)
    queryset = Comment.objects.all().filter(parent=None)
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = request.data.get('comment', {})
        serializer = self.serializer_class(data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, slug):
        serializer.save(author=self.request.user, slug=slug)

    def get(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = self.queryset.filter(slug=article_slug)
        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data)


class CommentsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=True)

    def destroy(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        instance = self.get_object()
        self.check_user(instance, request)
        self.perform_destroy(instance)
        return Response({"message": "Comment Deleted"}, status=status.HTTP_200_OK)

    def check_user(self, instance, request):
        if instance.author != request.user:
            raise PermissionDenied

    def update(self, request, *args, **kwargs):
        comment = request.data.get("comment", {})
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        instance = self.get_object()
        self.check_user(instance, request)
        serializer = self.get_serializer(instance, data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)


class CommentThreadListCreateView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentChildSerializer
    renderer_classes = (CommentThreadJSONRenderer,)
    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=False)

    def post(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        thread = request.data.get('comment', {})
        thread['parent'] = self.kwargs['id']
        serializer = self.serializer_class(data=thread, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, slug=slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = self.queryset.filter(
            slug=article_slug, parent=self.kwargs['id'])
        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)