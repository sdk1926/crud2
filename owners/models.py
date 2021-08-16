from django.db import models
from django.db.models.fields import EmailField

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=128)
    age = models.IntegerField()

    class Meta:
        db_table = 'owners'

    def __str__(self):
        return self.name

class Dog(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name='owner')
    name = models.CharField(max_length=45)
    age = models.IntegerField()

    class Meta:
        db_table = 'dogs'

    def __str__(self):
        return self.name