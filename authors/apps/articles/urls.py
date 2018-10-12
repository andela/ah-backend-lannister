from django.urls import path

from .views import (ArticleAPIView, ArticleAPIDetailsView, 
            RateArticleView, LikeArticleView, LikeAPIDetailsView, TagListAPIView, TagRetrieveAPIView)

app_name = "articles"

urlpatterns = [
    path("articles/", ArticleAPIView.as_view()),
    path('articles/<str:slug>/', ArticleAPIDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('articles/<str:slug>/rating/', RateArticleView.as_view()),
    path('articles/<str:slug>/like/',
         LikeArticleView.as_view(), name='like_article'),
    path('articles/<str:slug>/dislike/',
         LikeAPIDetailsView.as_view(), name='dislike'),
    path("tags/", TagListAPIView.as_view()),
    path("tags/<str:tag_name>/", TagRetrieveAPIView.as_view()),
]
