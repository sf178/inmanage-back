
# Create your models here.
from django.db import models
from datetime import datetime
from simple_history.models import HistoricalRecords


class Loans(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    data = models.DateTimeField(blank=True, null=True)
    insurance = models.BooleanField(default=False, blank=True)
    insurance_sum = models.FloatField(blank=True, null=True)
    remainder = models.FloatField(blank=True)
    sum = models.FloatField(blank=True) #loan sum
    loan_term = models.IntegerField(blank=True, null=True)
    percentage = models.FloatField(blank=True)
    month_payment = models.FloatField(blank=True)
    maintenance_cost = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Loan {self.name} of user with ID {self.user_id}'

    class Meta:
        verbose_name = 'loan'
        verbose_name_plural = 'loans'
        ordering = ('id',)


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    rent_type = models.BooleanField(blank=True)
    bought_price = models.FloatField(blank=True)
    actual_price = models.FloatField(blank=True)
    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    initial_payment = models.FloatField(blank=True, null=True)
    loan_term = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month_payment = models.FloatField(blank=True, null=True)
    #### loans part
    equipment_price = models.FloatField(blank=True)
    # month_income = models.FloatField()
    month_expense = models.FloatField(blank=True)
    average_consumption = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Property {self.name} of user with ID {self.user_id}'

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'
        ordering = ('id',)


class PropertyAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    price = models.FloatField()
    done = models.BooleanField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Asset {self.name} of property with ID {self.property}'

    class Meta:
        verbose_name = 'property_asset'
        verbose_name_plural = 'property_asset'
        ordering = ('id',)

class Transport(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, related_name='+')
    brand = models.TextField(blank=True)
    mark = models.TextField(blank=True)
    name = models.TextField(blank=True)
    model = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    owner_type = models.BooleanField(blank=True)
    vin = models.CharField(max_length=17, blank=True)
    use = models.TextField(blank=True)
    bought_price = models.FloatField(blank=True)
    average_market_price = models.FloatField(blank=True, null=True)
    min_market_price = models.FloatField(blank=True, null=True)
    max_market_price = models.FloatField(blank=True, null=True)

    #### loans part ####
    loan = models.BooleanField(blank=True, null=True)  # loan indicator
    initial_payment = models.FloatField(blank=True, null=True)
    loan_term = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month_payment = models.FloatField(blank=True, null=True)
    #### loans part

    month_expense = models.FloatField(blank=True, null=True)
    average_consumption = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()


    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'transport'
        verbose_name_plural = 'transport'
        ordering = ('id',)


class Passives(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    properties = models.ManyToManyField(Property, blank=True)
    transports = models.ManyToManyField(Transport, blank=True)
    loans = models.ManyToManyField(Loans, blank=True)

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        verbose_name = 'passives'
        verbose_name_plural = 'passives'
        ordering = ('id',)

