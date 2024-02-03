from django.db import transaction
from rest_framework import serializers
from .models import WorkIncome, Work
from balance.models import Card, Income
from balance.serializers import BalanceIncomeSerializer as IncomeSerializer

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'user', 'name']


class WorkIncomeSerializer(serializers.ModelSerializer):
    # Добавляем вложенные сериализаторы для Work и Project
    # work_data = WorkSerializer(source='work', required=False)
    #project_data = ProjectSerializer(source='project', required=False)

    class Meta:
        model = WorkIncome
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        work_data = validated_data.pop('work', None)
        work_instance = None

        # Создаем или получаем объект Work
        if isinstance(work_data, dict):
            # Если предоставлен словарь, создаем новый объект Work
            work_instance = Work.objects.create(**work_data, user=self.context['request'].user)
        elif isinstance(work_data, int):
            # Если предоставлен ID, получаем существующий объект Work
            work_instance = Work.objects.get(id=work_data, user=self.context['request'].user)

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
