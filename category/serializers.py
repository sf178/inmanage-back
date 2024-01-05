from rest_framework import serializers
from .models import *


class PersonalExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCategory
        fields = '__all__'


class ExpenseGeneralSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class GeneralExpenseCategorySerializer(serializers.ModelSerializer):
    subcategory = ExpenseGeneralSubcategorySerializer(required=False)

    class Meta:
        model = Category
        fields = '__all__'
