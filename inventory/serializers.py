from rest_framework import serializers
from .models import Inventory, InventoryAsset


class InventoryAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAsset
        fields= '__all__'


class InventorySerializer(serializers.ModelSerializer):
    assets = InventoryAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'
