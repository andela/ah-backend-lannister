from django.urls import path

from .views import (CommentListCreateView, CommentsView,
                    CommentThreadListCreateView)

app_name = 'comments'
urlpatterns = [
    path('<str:slug>/comments/', CommentListCreateView.as_view(),name='comments'),
    path('<str:slug>/comments/<int:id>', CommentsView.as_view(),name='indivdual comment'),
    path('<str:slug>/comments/<int:id>/thread', CommentThreadListCreateView.as_view(),name='thread comment'),
]
