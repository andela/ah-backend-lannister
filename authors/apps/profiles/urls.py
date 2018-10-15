from django.urls import path

from .views import ProfileRetrieveUpdateView, RetriveProfilesView, UnfollowView, FollowView

app_name ='profiles'

urlpatterns = [
    path('profiles/',RetriveProfilesView.as_view()),
    path('profiles/<str:username>/', ProfileRetrieveUpdateView.as_view()),
    path('profiles/<str:username>/follow/', FollowView.as_view()),
    path('profiles/<str:username>/unfollow/', UnfollowView.as_view()),
]

