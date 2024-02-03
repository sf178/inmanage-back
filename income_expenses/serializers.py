from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import WorkIncome, Work
from balance.models import Card, Income
from balance.serializers import BalanceIncomeSerializer as IncomeSerializer


class DynamicWorkField(serializers.Field):
    def to_representation(self, value):
        # Возвращаем представление объекта Work при сериализации
        return {'id': value.id, 'name': value.name}

    def to_internal_value(self, data):
        if isinstance(data, int):
            # Попытка получить существующую работу по ID
            try:
                return Work.objects.get(id=data, user=self.context['request'].user)
            except Work.DoesNotExist:
                raise ValidationError("Work with the given ID does not exist")
        elif isinstance(data, dict) and 'name' in data:
            # Создание новой работы, если предоставлен словарь с полем name
            work = Work.objects.create(**data, user=self.context['request'].user)
            return work
        else:
            raise ValidationError("Incorrect data for work field")


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'user', 'name']


class WorkIncomeSerializer(serializers.ModelSerializer):
    work = DynamicWorkField(required=False)
    # work_data = WorkSerializer(source='work', required=False)
    #project_data = ProjectSerializer(source='project', required=False)

    class Meta:
        model = WorkIncome
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        work_instance = validated_data.get('work')

        # Создаем или получаем объект Work
        # work_income = WorkIncome.objects.create(**validated_data)

        # Создаем объект WorkIncome
        work_income = WorkIncome.objects.create(**validated_data, work=work_instance)

        # Создаем связанный объект Income, если нужно
        if 'writeoff_account' in validated_data:
            writeoff_account = Card.objects.get(id=validated_data['writeoff_account'], user=self.context['request'].user)

            income = Income.objects.create(
                user=self.context['request'].user,
                writeoff_account=writeoff_account,
                funds=validated_data.get('funds', 0),
                comment=validated_data.get('comment', ''),
                content_object=work_income
            )
            writeoff_account.income.add(income)


        # Добавляем WorkIncome в income объекта Work, если он создан
        if work_instance:
            work_instance.income.add(work_income)

        return work_income
