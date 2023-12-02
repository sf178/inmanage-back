from rest_framework import serializers
from .models import *


class PersonalExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalExpenseCategory
        fields = ['id', 'title', 'icon_id', 'user']

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ['id', 'title', 'icon_id', 'asset_type']

class LiabilityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LiabilityCategory
        fields = ['id', 'title', 'icon_id', 'liability_type']



class ExpenseGeneralCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseGeneralCategory
        fields = ['id', 'name']

class ExpenseGeneralSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubCategory
        fields = ('id', 'name', 'general_category')
