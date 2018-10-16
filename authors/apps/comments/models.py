from django.db import models
from django.db.models.signals import post_save

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

    # null if the comment is a parent and has the parent id if its a child comment
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not True:
            return False
        return True


class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)


def create_history(sender, **kwargs):
    body = kwargs['instance'].body
    CommentHistory.objects.create(comment=kwargs['instance'], body=body)


post_save.connect(create_history, sender=Comment)
