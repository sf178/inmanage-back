from rest_framework import serializers
from .models import Loans, Property, PropertyAsset, Transport, Passives


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
    class Meta:
        model = Passives
        fields = '__all__'