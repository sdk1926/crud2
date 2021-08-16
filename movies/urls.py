from django.urls import path
from .views import ActorListView, MovieListView
urlpatterns = [
    path('/actor', ActorListView.as_view()),
    path('/movie', MovieListView.as_view()),
]