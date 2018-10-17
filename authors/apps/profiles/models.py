from django.db import models
from authors.apps.authentication.models import User
from datetime import datetime


class Profile(models.Model):

    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    image = models.URLField(default='https://i1.wp.com/www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png?fit=256%2C256&quality=100&ssl=1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.BooleanField(default=False)
    number_of_articles = models.IntegerField(default=0)
    favorites = models.ManyToManyField('articles.Article', related_name='favorited_by')
    app_notification_enabled = models.BooleanField(default=True)
    email_notification_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    def toggleFollowing(self):
        if self.following == True:
            return False
        return True

    def favorite(self, article):
        """Favorite an article"""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Unfavorite an article"""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Check if user has already favorited that article"""
        return self.favorites.filter(pk=article.pk).exists()


class FollowingUser(models.Model):
    """
    This a class to represent the relarionship between a user who is following an author
    """
    following_user = models.ForeignKey(
        "authentication.User", related_name='following_user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(
        "authentication.User", related_name='followed_user', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        """" This method saves the following """
        super(FollowingUser, self).save(**kwargs)

    def __str__(self):
        """ It retruns the string representation of a user following an author """
        return "{} is following {}".format(self.following_user, self.followed_user)

    class Meta:
        unique_together = (('followed_user', 'following_user'),)
        ordering = ['-date_added']
