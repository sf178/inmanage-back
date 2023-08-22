from rest_framework import serializers
from .models import *
from rest_framework_recursive.fields import RecursiveField
from test_backend.custom_methods import CustomDateTimeField


class InventoryAssetSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)
    class Meta:
        model = InventoryAsset
        fields= '__all__'


class InventoryExpensesSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)
    class Meta:
        model = InventoryExpenses
        fields= '__all__'


class PreviousInventorySerializer(serializers.ModelSerializer):
    assets = InventoryAssetSerializer(many=True, read_only=True)
    expenses = InventoryExpensesSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)
    class Meta:
        model = Inventory
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    assets = InventoryAssetSerializer(many=True, read_only=True)
    previous_inventories = PreviousInventorySerializer(many=True, read_only=True)
    expenses = InventoryExpensesSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)
    class Meta:
        model = Inventory
        fields = '__all__'


