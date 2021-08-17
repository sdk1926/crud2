from json import encoder
from json.decoder import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import json
import re
from django.http     import JsonResponse
from django.views    import View
from .models import Owner, Dog
# Create your views here.
class OwnerCreateView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            age      = data['age']
            goodmail = re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
                
            if not goodmail:
                return JsonResponse({'MESSAGE': 'NOT_EMAIL'}, status=400)

            owner = Owner(
                name  = name,
                email = email,
                age   = age
            )
            owner.save()
            return JsonResponse({'MESSAGE': 'CREATED'}, status=201)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        
        


class DogCreateView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            owner = data['owner']
            name  = data['name']
            age   = data['age']
            
            owner = Owner.objects.get(name=owner)

            dog = Dog(
                owner = owner,
                name  = name,
                age   = age
            )
            dog.save()
            return JsonResponse({'MESSAGE': 'CREATED'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE': 'NO_OWNER'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

            

                
class OwnerListView(View):
    def get(self, request):
        owners = Owner.objects.prefetch_related('owner').all()
        results = [
            {
                'name' : owner.name,
                'email': owner.email,
                'age'  : owner.age
            } for owner in owners
        ]
        results2 = [
            {
                'name' : owner.name,
                'email': owner.email,
                'age'  : owner.age,
                'dog'  :[
                    {
                    'name' : dog.name,  
                    'age' : dog.age,
                    }
                    for dog in owner.owner.all()
                ]
            }for owner in owners
        ]
        return JsonResponse({'result': results,'result2': results2}, status=200)

class DogListView(View):
    def get(self, request):
        dogs = Dog.objects.all()
        results = [
            {
                'owner': dog.owner.name,
                'name' : dog.name,
                'age'  : dog.age
            }
            for dog in dogs
        ]
        return JsonResponse({'result': results}, status=200)

        

        
        

