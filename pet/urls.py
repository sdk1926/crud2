from django.urls import path, include

urlpatterns = [
    path('ownerpet', include('owners.urls')),
]