import json
from django.http     import JsonResponse
from django.views    import View
from .models import Actor, Movie 
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class ActorListView(View):
    def get(self, request):
        actors = Actor.objects.prefetch_related('movies').all()
        results = [{
            "last_name"  : actor.last_name,
            "first_name" : actor.first_name,
            "movies"     : [
                movie.title
                for movie in actor.movies.all()]
            }for actor in actors]
        
        return JsonResponse({'result': results}, status=200)

class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.prefetch_related('actor').all()
        results = [{
            "title"        : movie.title,
            "running_time" : movie.running_time,
            "actor"        :[
                actor.last_name
                for actor in movie.actor.all()]
        }for movie in movies]

        return JsonResponse({'result': results}, status=200)

class MovieCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data['title']
            release_date = data['release_date']
            running_time = data['running_time']
            actor = data.get('actor',None)

            if Movie.objects.filter(title=title).exists():
                return JsonResponse({'MESSAGE': 'MOVIE_EXISTS'}, status=400)

            if actor:
                actor = Actor.objects.get(last_name=actor)
                movie = Movie.objects.create(
                    title = title,
                    release_date = release_date,
                    running_time = running_time
                )            
                movie.actor.add(actor)
            else:
                movie = Movie(
                    title = title,
                    release_date = release_date,
                    running_time = running_time
                )
                movie.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE': 'NO_ACTOR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)


class ActorCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            birth = data['birth']
            movie = data.get('movie',None)

            if movie:
                movie = Movie.objects.get(title=movie)
                actor = Actor.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    date_of_birth = birth
                )            
                actor.movies.add(movie)
            else:
                actor = Actor(
                    first_name = first_name,
                    last_name = last_name,
                    date_of_birth = birth
                )
                actor.save()
                
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE': 'NO_MOVIE'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)            
            


