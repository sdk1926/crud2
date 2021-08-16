import json
from django.http     import JsonResponse
from django.views    import View
from .models import Actor, Movie ,ActorMovie
# Create your views here.

class ActorListView(View):
    
    def get(self, request):
        actors = Actor.objects.prefetch_related('movies').all()
        results = [{
            "last_name" : actor.last_name,
            "first_name" : actor.first_name,
            "movies": [
                    movie.title
                for movie in actor.movies.all()]
            }for actor in actors]
        
        return JsonResponse({'result': results}, status=200)

class MovieListView(View):
    
    def get(self, request):
        movies = Movie.objects.prefetch_related('actor').all()
        results = [{
            "title": movie.title,
            "running_time": movie.running_time,
            "actor":[
                actor.last_name
            for actor in movie.actor.all()]
        }for movie in movies]

        return JsonResponse({'result': results}, status=200)

