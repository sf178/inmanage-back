from django.db import models
from front.models import CustomUser
from datetime import datetime
from simple_history.models import HistoricalRecords


# Create your models here.


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    done = models.BooleanField(blank=True, null=True, default=False)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    planned_sum = models.FloatField(blank=True, null=True)
    spent_sum = models.FloatField(blank=True, null=True)
    reserved_sum = models.FloatField(blank=True, null=True)
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tasks_list = models.ManyToManyField('TodoTask', related_name='+', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    income = models.ManyToManyField('todo.Income', blank=True, related_name='+')
    expenses = models.ManyToManyField('todo.Expenses', blank=True, related_name='+')
    expenses_is_completed = models.BooleanField(blank=True, null=True, default=False)
    history = HistoricalRecords()


    def __str__(self):
        return self.description


class TodoTask(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    desc_list = models.ManyToManyField('TodoItem', related_name='items', blank=True)
    expense = models.FloatField(blank=True, null=True)
    done = models.BooleanField(blank=True, null=True, default=False)
    income = models.ManyToManyField('todo.Income', blank=True, related_name='+')
    expenses = models.ManyToManyField('todo.Expenses', blank=True, related_name='+')
    expenses_is_completed = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()


    def __str__(self):
        return f'{self.id} - {self.title}'


class TodoItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(TodoTask, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True)
    done = models.BooleanField(blank=True, null=True, default=False)
    income = models.ManyToManyField('todo.Income', blank=True, related_name='+')
    expenses = models.ManyToManyField('todo.Expenses', blank=True, related_name='+')
    expenses_is_completed = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()


    def __str__(self):
        return self.id


class Planner(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    tasks = models.ManyToManyField(TodoTask)
    projects = models.ManyToManyField(Project)


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    task = models.ForeignKey('todo.TodoTask', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    item = models.ForeignKey('todo.TodoItem', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    project = models.ForeignKey('todo.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    task = models.ForeignKey('todo.TodoTask', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    item = models.ForeignKey('todo.TodoItem', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    project = models.ForeignKey('todo.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


