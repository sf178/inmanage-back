from django.db import models

# Create your models here.


class WorkIncome(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    work = models.ForeignKey('income_expenses.Work', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    project = models.ForeignKey('income_expenses.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True, default=0.0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True, null=True)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    name = models.TextField(blank=True, null=True)