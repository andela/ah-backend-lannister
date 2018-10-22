from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from authors.apps.articles.models import Article

from .models import Comment, CommentHistory, LikeComment
from .renderer import (CommentHistoryJSONRenderer, CommentJSONRenderer,
                       CommentThreadJSONRenderer)
from .serializers import (CommentChildSerializer, CommentHistorySerializer,
                          CommentSerializer, LikeCommentSerializer)
                          
from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.profiles.models import Profile
from authors.apps.notifications.models import notify_comment_follower


class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to create comments and retrieve comments 

    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    queryset = Comment.objects.all().filter(parent=None)
    queryset = Comment.objects.all()
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        """
        method to post a comment to article
        """
        comment, slug = self.get_comment_input(request)
        serializer = self.serializer_class(data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_comment_input(self, request):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = request.data.get('comment', {})
        if 'end_position' in comment and 'start_position' in comment:
            end_position = comment.get('end_position', 0)
            start_position = comment.get('start_position', 0)

            if type(end_position) != int or type(start_position) != int:
                raise ValidationError('one of the positions is not an integer')
            article_section = slug.body[start_position:end_position]
            comment['article_section'] = article_section
        return comment, slug

    def perform_create(self, serializer, slug):
        serializer.save(author=self.request.user, slug=slug)

    def get(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = self.queryset.filter(slug=article_slug)
        serializer = self.serializer_class(comment, many=True)
        return self.list(request, *args, **kwargs)


@receiver(post_save, sender=Comment)
def notify_follower_reciever(sender, instance, created, **kwargs):
    """
    Send a notification after the article being created is saved.
    """
    if created:
        message = (instance.author.username +
                   " has commented on an article that you favorited.")
        #import pdb;pdb.set_trace()
        
        article_id=instance.slug.id

        notify_comment_follower(article_id, message, instance)


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
        comment, slug = CommentListCreateView.get_comment_input(self, request)
        instance = self.get_object()
        self.check_user(instance, request)
        serializer = self.get_serializer(
            instance, data=comment, partial=True)
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


class CommentThreadListCreateView(generics.ListCreateAPIView):
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
        return self.list(request, *args, **kwargs)


class CommentHistoryView(generics.ListAPIView):
    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentHistoryJSONRenderer,)
    queryset = CommentHistory.objects.all()

    def get(self, request, *args, **kwargs):
        comment_history = self.queryset.filter(
            comment_id=self.kwargs['id'])
        if comment_history.count() < 2:
            return Response({"msg": "This comment has never been edited"})
        serializer = self.serializer_class(comment_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeCommentView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = LikeCommentSerializer

    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=True)

    def create(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['id'])

        if comment.author_id == request.user.id:
            return Response({"message": "you can't like your own comment"}, status=status.HTTP_400_BAD_REQUEST)

        instance = LikeComment.objects.filter(
            comment_id=comment.id, liked_by_id=request.user.id)
        if instance:
            return Response({"message": "you have already liked the comment"}, status=status.HTTP_400_BAD_REQUEST)
        comment.likes_count += 1

        comment.save()
        likes = comment.likes_count

        serializer = self.serializer_class(data=comment.__dict__)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, comment, likes)
        return Response(serializer.data)

    def perform_create(self, serializer, comment, likes):
        serializer.save(liked_by=self.request.user,
                        comment=comment, likes=likes)


class UnLikeCommentView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=True)

    def delete(self, request, *args, **kwargs):

        comment = get_object_or_404(Comment, id=self.kwargs['id'])

        try:
            instance = LikeComment.objects.get(
                comment_id=comment.id, liked_by_id=request.user.id)
        except:
            return Response({'message': 'This is not a comment you like.'},
                            status=status.HTTP_404_NOT_FOUND)

        if comment.likes_count > 0:
            comment.likes_count -= 1

        comment.save()
        instance.delete()
        serializer = self.serializer_class(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)
