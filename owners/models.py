from django.db import models
from django.db.models.fields import EmailField

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=128)
    age = models.IntegerField()

class Dog(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=45)
    age = models.IntegerField()