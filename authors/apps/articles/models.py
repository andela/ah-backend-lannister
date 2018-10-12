from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from authors.apps.authentication.models import User
from .utils import get_unique_slug,time

# Create your models here.


class Article(models.Model):
    """
    Model class for an Article
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False, blank=False)

    slug = models.SlugField(max_length=100, unique=True)

    description = models.TextField(null=False, blank=False)

    body = models.TextField(null=False, blank=False,)

    created_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    updated_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)

    favorited = models.BooleanField(default=False)

    favorites_count = models.IntegerField(default=0)

    read_time = models.TimeField(null=True, blank=True)

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
        read_time=time(self.body)
        return read_time


    class Meta:
        ordering = ['-created_at']

    
