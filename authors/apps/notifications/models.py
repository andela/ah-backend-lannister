from django.db import models
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comment
from authors.apps.profiles.models import FollowingUser


class Notification(models.Model):
    

    class Meta:
        
        ordering = ['-created_at']

    # article to send
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # notification message
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # users to be notified
    notified = models.ManyToManyField(
        User, related_name='notified', blank=True)
    # users that have read
    read = models.ManyToManyField(User, related_name='read', blank=True)
    classification = models.TextField(default="article")
    # check whether email has been sent
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        "Returns a string representation of notification."
        return self.notification


def notify_follower(author, notification, article):
    """
    Function that adds a article notification to the Notification model.

    """
    created_notification = Notification.objects.create(
        notification=notification, classification="article", article=article)

    userlist = FollowingUser.objects.filter(
        followed_user=author).values_list(
        'following_user', flat=True)
    followers = User.objects.filter(id__in=userlist)

    for follower in followers:
       
        if follower.profile.app_notification_enabled is True:
            created_notification.notified.add(follower.id)
    created_notification.save()


class CommentNotification(models.Model):
    

    class Meta:
       
        ordering = ['-created_at']

    # article to send
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    # notification message
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # users to be notified
    notified = models.ManyToManyField(
        User, related_name='comment_notified', blank=True)
    # users that have read
    read = models.ManyToManyField(
        User, related_name='comment_read', blank=True)
    classification = models.TextField(default="comment")
    # check whether email has been sent
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        "Returns a string representation of notification."
        return self.notification


def notify_comment_follower(article_id, notification, comment):
    """
    Function that adds a comment notification to the Notification model.

    """
    created_notification = CommentNotification.objects.create(
        notification=notification, classification="comment", comment=comment)

    followers = Profile.objects.filter(favorites=article_id)

    for follower in followers:
       
        if follower.app_notification_enabled is True:
            created_notification.notified.add(follower.id)
    created_notification.save()
