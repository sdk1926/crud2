from django.urls import path, include

urlpatterns = [
    #path('ownerpet', include('owners.urls')),
    path('movie', include('movies.urls'))
]