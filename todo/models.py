from django.db import models
from front.models import CustomUser
from datetime import datetime
from simple_history.models import HistoricalRecords
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.

# def validate_color_hex(value):
#     """
#     Проверка, что значение соответствует HEX-формату для цветов.
#     """
#     if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
#         raise ValidationError(
#             _('%(value)s is not a valid HEX color.'),
#             params={'value': value},
#         )

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
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
    total_income = models.FloatField(blank=True, null=True)
    total_expenses = models.FloatField(blank=True, null=True)
    expenses_is_completed = models.BooleanField(blank=True, null=True, default=False)
    history = HistoricalRecords()


    def __str__(self):
        return self.description


class TodoTask(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    desc_list = models.ManyToManyField('TodoItem', related_name='items', blank=True)
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


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    task = models.ForeignKey('todo.TodoTask', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    item = models.ForeignKey('todo.TodoItem', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    project = models.ForeignKey('todo.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    # category = models.ForeignKey('category.PersonalCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    child = models.ForeignKey('balance.Income', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    funds = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    task = models.ForeignKey('todo.TodoTask', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    item = models.ForeignKey('todo.TodoItem', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    project = models.ForeignKey('todo.Project', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    # category = models.ForeignKey('category.PersonalCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    child = models.ForeignKey('balance.Expenses', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Planner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    projects = models.ManyToManyField('todo.Project', blank=True, related_name='planners')
    tasks = models.ManyToManyField('todo.TodoTask', blank=True, related_name='tasks')
    total_income = models.FloatField(blank=True, null=True, default=0.0)
    total_expenses = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_totals(self):
        # Обновляем общие доходы и расходы
        self.total_income = sum(project.total_income for project in self.projects.all() if project.total_income)
        self.total_expenses = sum(project.total_expenses for project in self.projects.all() if project.total_expenses)
        self.save()

    def __str__(self):
        return f"Planner ID: {self.id} - Total Income: {self.total_income} - Total Expenses: {self.total_expenses}"


# class MainTasks(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, related_name='+')
#     total_funds = models.FloatField(blank=True, null=True, default=0.0)
#     total_income = models.FloatField(blank=True, null=True, default=0.0)
#     total_expenses = models.FloatField(blank=True, null=True, default=0.0)
#     tasks = models.ManyToManyField(TodoTask, blank=True, null=True)
#     def __str__(self):
#         return f'ID: {self.id}'