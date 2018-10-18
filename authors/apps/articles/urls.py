from django.urls import path

from .views import (
    ArticleAPIView, ArticleAPIDetailsView, 
    RateArticleView, LikeArticleView, LikeAPIDetailsView,
    TagListAPIView, TagRetrieveAPIView, CategoryListCreateAPIView,
    CategoryRetrieveAPIView, FavoriteArticleView, UnFavoriteArticleView,
    ShareArticleAPIView,)

app_name = "articles"

urlpatterns = [
    path("articles/", ArticleAPIView.as_view()),
    path('articles/<str:slug>/', ArticleAPIDetailsView.as_view(),
         name='retrieveUpdateDelete'),
    path('articles/<str:slug>/rating/', RateArticleView.as_view()),
    path('articles/<str:slug>/like/',
         LikeArticleView.as_view(), name='like_article'),
    path('articles/<str:slug>/share/',
         ShareArticleAPIView.as_view(), name='share_article'),
    path('articles/<str:slug>/dislike/',
         LikeAPIDetailsView.as_view(), name='dislike'),
    path("tags/", TagListAPIView.as_view()),
    path("tags/<str:tag_name>/", TagRetrieveAPIView.as_view()),
    path("categories/", CategoryListCreateAPIView.as_view()),
    path("categories/<str:cat_name>/", CategoryRetrieveAPIView.as_view()),
    path('articles/<str:slug>/favorite/', FavoriteArticleView.as_view(), name="favorite"),
    path('articles/<str:slug>/unfavorite/', UnFavoriteArticleView.as_view(), name="unfavorite")


]
