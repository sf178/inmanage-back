from django.db import models
from front.models import CustomUser
from simple_history.models import HistoricalRecords

# Create your models here.


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    bank = models.BooleanField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True, default=None)
    card_num = models.TextField(max_length=16, blank=True, null=True, default=None)
    loan = models.BooleanField(blank=True, null=True)
    interest_free = models.FloatField(blank=True, null=True, default=None)
    percentage = models.FloatField(blank=True, null=True, default=None)
    remainder = models.FloatField(blank=True, null=True, default=None)
    limit = models.FloatField(blank=True, null=True, default=None)
    flag = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        ordering = ('id',)


class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    total_in_currency = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    card_list = models.ManyToManyField(Card, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'balance'
        verbose_name_plural = 'balance'
        ordering = ('id',)
