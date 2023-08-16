from rest_framework import serializers
from .models import *


class ExpensePersonalSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensePersonalSubcategory
        fields = ['name']


class ExpensePersonalCategorySerializer(serializers.ModelSerializer):
    subcategories = ExpensePersonalSubcategorySerializer(many=True)

    class Meta:
        model = ExpensePersonalCategory
        fields = ['name', 'subcategories']


class ExpenseGeneralNestedSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseGeneralNestedSubCategory
        fields = ['name']


class ExpenseGeneralSubCategorySerializer(serializers.ModelSerializer):
    nested_subcategories = ExpenseGeneralNestedSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ExpenseGeneralSubCategory
        fields = ['name', 'nested_subcategories']


class ExpenseGeneralCategorySerializer(serializers.ModelSerializer):
    subcategories = ExpenseGeneralSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ExpenseGeneralCategory
        fields = ['name', 'subcategories']