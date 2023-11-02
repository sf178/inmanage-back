from rest_framework import serializers
from .models import *


class ExpensePersonalCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpensePersonalCategory
        fields = ['id', 'name']




class ExpenseGeneralCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseGeneralCategory
        fields = ['id', 'name']

class ExpenseGeneralSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubCategory
        fields = ('id', 'name', 'general_category')
