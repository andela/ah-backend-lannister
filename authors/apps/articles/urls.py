from django.urls import path

from .views import ArticleAPIView, ArticleAPIDetailsView

app_name = "articles"

urlpatterns = [
    path("articles/", ArticleAPIView.as_view()),
    path('articles/<str:slug>/', ArticleAPIDetailsView.as_view(),name='retrieveUpdateDelete'),
]