from rest_framework import serializers
from .models import *


class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAsset
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


class PassivesSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    transports = TransportSerializer(many=True, read_only=True)
    class Meta:
        model = Passives
        fields = '__all__'


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('id', 'property', 'transport', 'funds', 'created_at')
