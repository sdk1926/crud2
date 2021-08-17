from json import encoder
from django.shortcuts import render
import json
import re
from django.http     import JsonResponse
from django.views    import View
from .models import Owner, Dog
from django.db import transaction
# Create your views here.
class OwnerCreateView(View):
    def post(self, request):
        if request.META['CONTENT_TYPE'] == "application/json":            
            try:
                data  = json.loads(request.body)
            except:
                return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, staus=400)

            name  = data.get('name',None)
            email = data.get('email', None)
            age   = data.get('age', None)

            if name and email and age:
                goodmail = re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
                if not goodmail:
                    return JsonResponse({'MESSAGE': 'NOT_EMAIL'}, status=400)
                try:
                    with transaction.atomic():
                        o = Owner(
                            name  = name,
                            email = email,
                            age   = age
                        )
                        o.save()
                except:
                    return JsonResponse({'MESSAGE': 'FAILED'}, status=400)
                else:
                    return JsonResponse({'MESSAGE': 'CREATED'}, status=201)
            else:
                return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        else:
            return JsonResponse({'MESSAGE': 'NOT_JSON'}, status=400)

class DogCreateView(View):
    def post(self, request):
        if request.META['CONTENT_TYPE'] == "application/json":
            try:
                data  = json.loads(request.body)
            except:
                return JsonResponse({'MESSAGE': 'VALUE_ERROR'})

            owner = data.get('owner', None)
            name  = data.get('name', None)
            age   = data.get('age', None)

            if owner and name and age:
                try:
                    owner = Owner.objects.get(name=owner)
                except:
                    return JsonResponse({'MESSAGE': 'NO_OWNER'}, status=400)
                try:
                    with transaction.atomic():
                        d = Dog(
                            owner = owner,
                            name  = name,
                            age   = age
                            )
                        d.save()
                except:
                    return JsonResponse({'MESSAGE': 'FAILED'}, status=400)
                else:    
                    return JsonResponse({'MESSAGE': 'CREATED'}, status=201)     
            else:   
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

        

        
        

