from rest_framework import serializers
from .models import *
from passives import serializers as pas
from inventory import serializers as inv
import json


def serialize_object_to_json(obj):
    return json.dumps(obj, default=str)


class PropertySerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)
    equipment = inv.InventorySerializer(many=False, required=False)
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
        try:
            instance.average_profit = instance.month_income - instance.month_expense - instance.month_payment
        except:
            instance.average_profit = 0
        instance.save()
        return instance


class TransportSerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)

    class Meta:
        model = Transport
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)
    equipment = inv.InventorySerializer(many=False, required=False)

    class Meta:
        model = Business
        fields = '__all__'


class ActivesIncomeSerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False, allow_null=True)
    transport = TransportSerializer(required=False, allow_null=True)
    business = BusinessSerializer(required=False, allow_null=True)

    class Meta:
        model = ActivesIncome
        fields = ('id', 'property', 'transport', 'business', 'funds', 'created_at')


class ActivesExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivesExpenses
        fields = ('id', 'property', 'transport', 'business', 'funds', 'created_at')


class MainPropertySerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainProperties
        fields = '__all__'


class MainBusinessesSerializer(serializers.ModelSerializer):
    businesses = BusinessSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainBusinesses
        fields = '__all__'


class MainTransportSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainTransport
        fields = '__all__'


class ActivesSerializer(serializers.ModelSerializer):
    properties = MainPropertySerializer(read_only=True, required=False, allow_null=True)
    transports = MainTransportSerializer(read_only=True, required=False, allow_null=True)
    businesses = MainBusinessesSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Actives
        fields = '__all__'


PropertySerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
PropertySerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
BusinessSerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
BusinessSerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)

