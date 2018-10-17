from django.urls import path

from .views import (AllBookmarksView, ArticleAPIDetailsView, ArticleAPIView,
                    BookmarkView, CategoryListCreateAPIView,
                    CategoryRetrieveAPIView, FavoriteArticleView,
                    LikeAPIDetailsView, LikeArticleView, RateArticleView,
                    ReportArticle, ReportArticleListView, ReportView,
                    ShareArticleAPIView, TagListAPIView, TagRetrieveAPIView,
                    UnBookmarkView, UnFavoriteArticleView)

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
    path('articles/<str:slug>/favorite/',
         FavoriteArticleView.as_view(), name="favorite"),
    path('articles/<str:slug>/unfavorite/',
         UnFavoriteArticleView.as_view(), name="unfavorite"),
    path('articles/<str:slug>/report/', ReportArticle.as_view(), name="escalate"),
    path('escalations/', ReportArticleListView.as_view(), name="escalated"),
    path('escalations/report/', ReportView.as_view(), name="escalatation report"),


    path('articles/<str:slug>/bookmark/', BookmarkView.as_view(),
         name='bookmark_articles'),
    path('articles/<str:slug>/unbookmark/', UnBookmarkView.as_view(),
         name='unbookmark_articles'),
    path('bookmarks/', AllBookmarksView.as_view(),
         name='bookmarks'),

]
