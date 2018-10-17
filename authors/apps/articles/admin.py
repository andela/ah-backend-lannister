from django.contrib import admin

from authors.apps.articles.models import (Article, Category, LikeArticle,
                                          RateArticle, Reported,Bookmark)

admin.site.register(Article)
admin.site.register(RateArticle)
admin.site.register(LikeArticle)
admin.site.register(Category)
admin.site.register(Reported)
admin.site.register(Bookmark)
