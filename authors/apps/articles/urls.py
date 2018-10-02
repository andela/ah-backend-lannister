from django.urls import path

from .views import ArticleAPIView

app_name = "articles"

urlpatterns = [
    path("articles/", ArticleAPIView.as_view()),
]