from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.utils.text import slugify

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from taggit.managers import TaggableManager

from .utils import get_unique_slug, time


class Category(models.Model):
    title = models.CharField(max_length=100, default="general")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        return super().save(*args, **kwargs)


class Article(models.Model):
    """
    Model class for an Article
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False, blank=False)

    slug = models.SlugField(max_length=100, unique=True)

    description = models.TextField(null=False, blank=False)

    body = models.TextField(null=False, blank=False,)

    image = models.URLField(blank=True)

    created_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    updated_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    favorited = models.BooleanField(default=False)

    favorites_count = models.IntegerField(default=0)

    read_time = models.TimeField(null=True, blank=True)

    tags = TaggableManager()

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    times_reported = models.IntegerField(default=0)

    is_published = models.BooleanField(default=False)

    published_on = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    def __str__(self):
        """
        Returns a string representation of this `Article`.

        This string is used when a `Article` is printed in the console.
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        return super().save(*args, **kwargs)

    def read(self):
        read_time = time(self.body)
        return read_time

    class Meta:
        ordering = ['-created_at']

    def average_rating(self):
        ratings = RateArticle.objects.filter(
            article=self).aggregate(Avg('rating'))
        if ratings['rating__avg'] == None:
            return 0
        else:
            return int(ratings['rating__avg'])

    def like_cal(self, like):
        total_likes = LikeArticle.objects.filter(
            article=self, likes=like).count()
        return total_likes

    def likes(self):
        return self.like_cal(True)

    def dislikes(self):
        return self.like_cal(False)


class RateArticle(models.Model):
    rated_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey(Article, blank=False, on_delete=models.CASCADE)

    rating = models.IntegerField(blank=False, null=False, default=0)


class LikeArticle(models.Model):
    liked_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    article = models.ForeignKey(Article, blank=False, on_delete=models.CASCADE)

    likes = models.NullBooleanField()


class Reported(models.Model):
    article = models.ForeignKey(
        Article, blank=False, on_delete=models.CASCADE, to_field='slug')
    user = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE, to_field='email')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

        
class Bookmark(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    slug = models.ForeignKey(Article,blank=False, on_delete=models.CASCADE, to_field='slug')
    bookmarked_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)
