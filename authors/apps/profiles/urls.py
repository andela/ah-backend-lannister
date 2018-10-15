from django.urls import path

from .views import ProfileRetrieveUpdateView, RetriveProfilesView

app_name ='profiles'

urlpatterns = [
    path('profiles/',RetriveProfilesView.as_view()),
    path('profiles/<str:username>/', ProfileRetrieveUpdateView.as_view()),
]

