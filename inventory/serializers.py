from rest_framework import serializers
from .models import Inventory, InventoryAsset
from rest_framework_recursive.fields import RecursiveField


class InventoryAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAsset
        fields= '__all__'


class InventorySerializer(serializers.ModelSerializer):
    assets = InventoryAssetSerializer(many=True, read_only=True)
    previous_inventories = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'
