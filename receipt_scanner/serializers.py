# serializers.py
from rest_framework import serializers
from .models import Receipt, ReceiptItem


class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True, required=False)

    class Meta:
        model = Receipt
        fields = '__all__'
