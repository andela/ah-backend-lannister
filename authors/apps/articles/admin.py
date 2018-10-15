from django.contrib import admin
from authors.apps.articles.models import Article, RateArticle, LikeArticle
admin.site.register(Article)
admin.site.register(RateArticle)
admin.site.register(LikeArticle)
