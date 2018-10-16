from django.contrib import admin
from authors.apps.articles.models import Article, RateArticle, LikeArticle, Category
admin.site.register(Article)
admin.site.register(RateArticle)
admin.site.register(LikeArticle)
admin.site.register(Category)
