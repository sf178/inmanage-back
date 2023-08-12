from rest_framework import serializers
from .models import ExpenseCategory, ExpenseSubcategory


class ExpenseSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubcategory
        fields = ['name']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    subcategories = ExpenseSubcategorySerializer(many=True)

    class Meta:
        model = ExpenseCategory
        fields = ['name', 'subcategories']