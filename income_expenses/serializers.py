from rest_framework import serializers
from .models import WorkIncome, Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'user', 'name']


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'user', 'name']


class WorkIncomeSerializer(serializers.ModelSerializer):
    # Добавляем вложенные сериализаторы для Work и Project
    work_data = WorkSerializer(source='work', required=False)
    # project_data = ProjectSerializer(source='project', required=False)

    class Meta:
        model = WorkIncome
        fields = ['id', 'user', 'work', 'project', 'funds', 'comment', 'created_at', 'work_data', 'project_data']

    def create(self, validated_data):
        work_data = validated_data.pop('work', None)
        project_data = validated_data.pop('project', None)

        if work_data:
            work = Work.objects.create(**work_data)
            validated_data['work'] = work

        if project_data:
            project = Project.objects.create(**project_data)
            validated_data['project'] = project

        return WorkIncome.objects.create(**validated_data)
