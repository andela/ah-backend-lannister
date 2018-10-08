from django.db import models
from authors.apps.authentication.models import User

class Profile(models.Model):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.BooleanField(default=False)
    number_of_articles = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username