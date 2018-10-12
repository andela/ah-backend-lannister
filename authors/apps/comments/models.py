from django.db import models

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

# Create your models here.


class Comment(models.Model):
    # this has the aothor of the comment
    # references user in user table
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    slug = models.ForeignKey(
        Article, on_delete=models.CASCADE, to_field='slug')
    # the content of the comment
    body = models.TextField()

    # true if the comment is a parent and false if its a child comment
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = CommentManager()

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not True:
            return False
        return True
