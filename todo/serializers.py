from rest_framework import serializers
from .models import *
from test_backend.custom_methods import CustomDateTimeField
created_at = CustomDateTimeField(required=False)

class TodoIncomeSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Income
        fields = ('id', 'created_at')


class TodoExpensesSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Expenses
        fields = ('id', 'created_at')


class TodoItemSerializer(serializers.ModelSerializer):
    income = TodoIncomeSerializer(many=True, read_only=True)
    expenses = TodoExpensesSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = TodoItem
        fields = '__all__'


class TodoTaskSerializer(serializers.ModelSerializer):
    desc_list = TodoItemSerializer(many=True, read_only=True)
    income = TodoIncomeSerializer(many=True, read_only=True)
    expenses = TodoExpensesSerializer(many=True, read_only=True)
    date_start = CustomDateTimeField(required=False)
    date_end = CustomDateTimeField(required=False)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = TodoTask
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tasks_list = TodoTaskSerializer(many=True, read_only=True)
    income = TodoIncomeSerializer(many=True, read_only=True)
    expenses = TodoExpensesSerializer(many=True, read_only=True)
    date_start = CustomDateTimeField(required=False)
    date_end = CustomDateTimeField(required=False)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Project
        fields = '__all__'


class PlannerSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    tasks = TodoTaskSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Planner
        fields = '__all__'
