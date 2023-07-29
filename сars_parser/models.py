# Create your models here.
from django.db import models


class Car(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    cyrillic_name = models.CharField(max_length=200)
    popular = models.BooleanField(default=False)
    country = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Model(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    cyrillic_name = models.CharField(max_length=200)
    car_class = models.CharField(max_length=50)
    year_from = models.IntegerField()
    year_to = models.IntegerField()
    car = models.ForeignKey(Car, related_name='models', on_delete=models.CASCADE)

    def __str__(self):
        return self.name