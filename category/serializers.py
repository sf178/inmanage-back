from rest_framework import serializers
from .models import *

class ExpenseSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensePersonalSubcategory
        fields = ['name']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    subcategories = ExpenseSubcategorySerializer(many=True)

    class Meta:
        model = ExpensePersonalCategory
        fields = ['name', 'subcategories']