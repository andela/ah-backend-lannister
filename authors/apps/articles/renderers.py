"""
Renderer classes go here
"""
from authors.apps.renderer import AhJSONRenderer


class ArticleJSONRenderer(AhJSONRenderer):
    object_label = 'article'
    charset = 'utf-8'

class TagJSONRenderer(AhJSONRenderer):
    object_label = 'tag'
    charset = 'utf-8'


class LikeUserJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'like'


class RateUserJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'rate'


class CategoryJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'category'


class ShareArticleJSONRenderer(AhJSONRenderer):
    charset = 'utf-8'
    object_label = 'share'


