from django.db import models
from front.models import CustomUser
from simple_history.models import HistoricalRecords

# Create your models here.


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    bank = models.BooleanField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True, default=None)
    card_num = models.TextField(max_length=16, blank=True, null=True, default=None)
    loan = models.BooleanField(blank=True, null=True)
    interest_free = models.FloatField(blank=True, null=True, default=None)
    percentage = models.FloatField(blank=True, null=True, default=None)
    remainder = models.FloatField(blank=True, null=True, default=None)
    limit = models.FloatField(blank=True, null=True, default=None)
    flag = models.BooleanField(blank=True, null=True, default=False)
    incomes = models.ManyToManyField('Income', blank=True, related_name='+')
    expenses = models.ManyToManyField('Expenses', blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField(upload_to='bank_images/', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        ordering = ('id',)


class Balance(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    total = models.FloatField(blank=True, null=True)
    total_in_currency = models.FloatField(blank=True, null=True)
    total_income = models.FloatField(blank=True, null=True)
    total_expenses = models.FloatField(blank=True, null=True)
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


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
