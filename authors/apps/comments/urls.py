from django.urls import path

from .views import (CommentListCreateView, CommentsView,
                    CommentThreadListCreateView, CommentHistoryView,LikeCommentView, UnLikeCommentView)

app_name = 'comments'
urlpatterns = [
    path('<str:slug>/comments/', CommentListCreateView.as_view(),name='comments'),
    path('<str:slug>/comments/<int:id>', CommentsView.as_view(),name='indivdual comment'),
    path('<str:slug>/comments/<int:id>/thread', CommentThreadListCreateView.as_view(),name='thread comment'),
    path('<str:slug>/comments/<int:id>/edit-history/', CommentHistoryView.as_view(),name='edit history'),
    path('<str:slug>/comments/<int:id>/like', LikeCommentView.as_view(),name='like comment'),
    path('<str:slug>/comments/<int:id>/unlike', UnLikeCommentView.as_view(),name='unlike comment'),

]
