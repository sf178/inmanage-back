from rest_framework import serializers
from .models import *
import json


def serialize_object_to_json(obj):
    return json.dumps(obj, default=str)



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.actual_price = validated_data.get('actual_price', instance.actual_price)
        instance.bought_price = validated_data.get('bought_price', instance.bought_price)
        instance.initial_payment = validated_data.get('initial_payment', instance.initial_payment)
        instance.loan_term = validated_data.get('loan_term', instance.loan_term)
        instance.rent_type = validated_data.get('rent_type', instance.rent_type)
        instance.percentage = validated_data.get('percentage', instance.percentage)
        instance.month_payment = validated_data.get('month_payment', instance.month_payment)
        instance.revenue = validated_data.get('revenue', instance.revenue)
        instance.equipment_price = validated_data.get('equipment_price', instance.equipment_price)
        instance.month_income = validated_data.get('month_income', instance.month_income)
        instance.month_expense = validated_data.get('month_expense', instance.month_expense)
        instance.average_profit = instance.month_income - instance.month_expense - instance.month_payment
        instance.save()
        return instance


class PropertyAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAsset
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class BusinessAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAsset
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'


class BondsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = '__all__'


class ActivesSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    transports = TransportSerializer(many=True, read_only=True)
    businesses = BusinessSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)
    obligations = BondsSerializer(many=True, read_only=True)

    class Meta:
        model = Actives
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False, allow_null=True)
    transport = TransportSerializer(required=False, allow_null=True)
    business = BusinessSerializer(required=False, allow_null=True)

    class Meta:
        model = Income
        fields = ('id', 'property', 'transport', 'business', 'funds', 'created_at')

class ExpensesSerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False, allow_null=True)
    transport = TransportSerializer(required=False, allow_null=True)
    business = BusinessSerializer(required=False, allow_null=True)

    class Meta:
        model = Expenses
        fields = ('id', 'property', 'transport', 'business', 'funds', 'created_at')

# class PassivesSerializer(serializers.ModelSerializer):
#     properties = PropertySerializer(many=True, read_only=True)
#     transports = TransportSerializer(many=True, read_only=True)
#     # добавить loans - кредиты и займы
#
#
#     class Meta:
#         model = Passives
#         fields = '__all__'


# class ProfileSerializer(serializers.ModelSerializer):
#     cards = CardSerializer(many=True, read_only=True)
#     actives = ActivesSerializer(many=True, read_only=True)
#     passives = PassivesSerializer(many=True, read_only=True)
#
#
#     class Meta:
#         model = ObjectsProfile
#         fields = '__all__'

