"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
import debug_toolbar

schema_view = get_swagger_view(title="Authors Haven API ")
from authors.apps.social_auth.views import (FacebookLogin,
                                            TwitterLogin,
                                            GoogleLogin)



urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authors.apps.authentication.urls',
                         namespace='authentication')),
    path('api/', include('authors.apps.profiles.urls', namespace='profiles')),
    path('api/', include('authors.apps.articles.urls', namespace='articles')),
    path('api/articles/', include('authors.apps.comments.urls', namespace='comments')),
    path('api/notifications/', include('authors.apps.notifications.urls', namespace='notifications')),

    path('', RedirectView.as_view(url='coreapi-docs/'), name='index'),
    path('swagger-docs/', schema_view),
    path('coreapi-docs/', include_docs_urls(title='Authors Haven API')),
    path('__debug__/', include(debug_toolbar.urls)),
    
    
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    # path('accounts/login/', include('authors.apps.social_auth.urls')),
    path('accounts/', include('allauth.urls')),


]

