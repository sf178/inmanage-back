# Create your models here.
from django.db import models


class Car(models.Model):
    mark = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    href = models.URLField(blank=True, null=True)
    average_price = models.CharField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    km_age = models.CharField(blank=True, null=True)

    def __str__(self):
        return f'{self.mark} {self.model}'
