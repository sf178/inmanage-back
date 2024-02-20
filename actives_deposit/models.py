from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.
# class ActivesLoans(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True)
#     date = models.DateTimeField(blank=True, null=True)
#     insurance = models.BooleanField(default=False, blank=True)
#     insurance_sum = models.FloatField(blank=True, null=True, default=0.0)
#     remainder = models.FloatField(blank=True, null=True, default=0.0)
#     sum = models.FloatField(blank=True, null=True, default=0.0) #loan sum
#     loan_term = models.BigIntegerField(blank=True, null=True)
#     percentage = models.FloatField(blank=True, null=True, default=0.0)
#     month_payment = models.FloatField(blank=True, null=True, default=0.0)
#     maintenance_cost = models.FloatField(blank=True, null=True, default=0.0)
#     expenses = models.ManyToManyField('actives.ActivesExpenses', blank=True, null=True, related_name='+')
#     total_expense = models.FloatField(blank=True, null=True, default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='bank_images/', blank=True, null=True)
#     history = HistoricalRecords()
#
#     def __str__(self):
#         return f'Loan {self.name} of user with ID {self.user_id}'
#
#     class Meta:
#         verbose_name = 'loan'
#         verbose_name_plural = 'loans'
#         ordering = ('id',)


class ActivesDeposit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    #name = models.CharField(max_length=255, blank=True)
    type = models.TextField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    incomes = models.ManyToManyField('actives.ActivesIncome', blank=True, null=True, related_name='+')
    percentage = models.FloatField(blank=True, null=True, default=0.0)
    sum = models.FloatField(blank=True, null=True, default=0.0) #loan sum

