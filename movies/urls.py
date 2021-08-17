from django.urls import path
from .views import ActorListView, MovieCreateView, MovieListView, ActorCreateView
urlpatterns = [
    path('/actor', ActorListView.as_view()),
    path('/movie', MovieListView.as_view()),
    path('/movie/1', MovieCreateView.as_view()),
    path('/actor/1', ActorCreateView.as_view())
]