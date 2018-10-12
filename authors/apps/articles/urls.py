from django.urls import path

from .views import ArticleAPIView, ArticleAPIDetailsView, RateArticleView

app_name = "articles"

urlpatterns = [
    path("articles/", ArticleAPIView.as_view()),
    path('articles/<str:slug>/', ArticleAPIDetailsView.as_view(),name='retrieveUpdateDelete'),
    path('articles/<str:slug>/rating/', RateArticleView.as_view())
]