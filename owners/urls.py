from django.urls import path

from owners.views import OwnerCreateView, DogCreateView, OwnerListView, DogListView

urlpatterns = [
	path('/owner/1', OwnerCreateView.as_view()),
    path('/dog/1', DogCreateView.as_view()),
    path('/owner', OwnerListView.as_view()),
    path('/dog', DogListView.as_view()),
]