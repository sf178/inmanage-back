from rest_framework import serializers
from .models import *


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('id', 'created_at')


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('id', 'created_at')


class TodoItemSerializer(serializers.ModelSerializer):
    income = IncomeSerializer(many=True)
    expenses = ExpensesSerializer(many=True)
    class Meta:
        model = TodoItem
        fields = '__all__'


class TodoTaskSerializer(serializers.ModelSerializer):
    desc_list = TodoItemSerializer(many=True, read_only=True)
    income = IncomeSerializer(many=True)
    expenses = ExpensesSerializer(many=True)

    class Meta:
        model = TodoTask
        fields = '__all__'

    # def create(self, validated_data):
    #     project_id = validated_data.pop('project_id')
    #     task = TodoTask.objects.create(**validated_data)
    #     project = Project.objects.get(id=project_id)
    #     project.tasks.add(task)
    #     return task


class ProjectSerializer(serializers.ModelSerializer):
    tasks_list = TodoTaskSerializer(many=True, read_only=True)
    income = IncomeSerializer(many=True)
    expenses = ExpensesSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'


