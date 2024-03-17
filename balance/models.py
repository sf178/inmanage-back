from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from front.models import CustomUser
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
# Create your models here.


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name or ''


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    # is_paid = models.BooleanField(default=False)
    is_paid = JSONField(default=dict, blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name or ''


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    bank = models.BooleanField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True, default=None)
    card_num = models.TextField(max_length=16, blank=True, null=True, default=None)
    loan = models.BooleanField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    interest_free = models.FloatField(blank=True, null=True, default=None)
    percentage = models.FloatField(blank=True, null=True, default=None)
    remainder = models.FloatField(blank=True, null=True, default=0.0)
    limit = models.FloatField(blank=True, null=True, default=None)
    flag = models.BooleanField(blank=True, null=True, default=False)
    income = models.ManyToManyField('Income', blank=True, related_name='+')
    total_income = models.FloatField(blank=True, null=True, default=None)
    expenses = models.ManyToManyField('Expenses', blank=True, related_name='+')
    total_expense = models.FloatField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_editable = models.BooleanField(blank=True, null=True, default=True)
    is_business = models.BooleanField(blank=True, null=True, default=False)
    is_deletable = models.BooleanField(blank=True, null=True, default=True)
    is_visible = models.BooleanField(blank=True, null=True, default=True)

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
    daily_income = models.FloatField(blank=True, null=True, default=0.0)
    daily_expense = models.FloatField(blank=True, null=True, default=0.0)
    monthly_income = models.FloatField(blank=True, null=True, default=0.0)
    monthly_expense = models.FloatField(blank=True, null=True, default=0.0)
    currency = models.TextField(blank=True, null=True)
    card_list = models.ManyToManyField(Card, blank=True, null=True, related_name='+')
    favourite_cards = models.ManyToManyField(Card, blank=True, null=True, related_name='+')
    payments = models.ManyToManyField(Payment, blank=True, null=True, related_name='+')
    card_funds = models.FloatField(blank=True, null=True)
    card_income = models.FloatField(blank=True, null=True)
    card_expenses = models.FloatField(blank=True, null=True)
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
    # card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    # category = models.ForeignKey('category.PersonalCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    # card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    category = models.ForeignKey('category.PersonalCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    funds = models.FloatField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
