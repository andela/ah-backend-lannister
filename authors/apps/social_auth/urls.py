from django.urls import path
from .views import FacebookLogin, TwitterLogin



app_name = 'social_auth'

urlpatterns = [
    path('facebook/', FacebookLogin.as_view(), name='login'),
]