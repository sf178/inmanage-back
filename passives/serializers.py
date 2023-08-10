from rest_framework import serializers
from .models import *


class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    loan_link = LoansSerializer(many=False, required=False)

    class Meta:
        model = Property
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    loan_link = LoansSerializer(many=False, required=False)

    class Meta:
        model = Transport
        fields = '__all__'


class MainPropertiesSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainProperties
        fields = '__all__'


class MainLoansSerializer(serializers.ModelSerializer):
    loans = LoansSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainLoans
        fields = '__all__'


class MainTransportSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = MainTransport
        fields = '__all__'


class PassivesSerializer(serializers.ModelSerializer):
    properties = MainPropertiesSerializer(read_only=True, required=False, allow_null=True)
    transports = MainTransportSerializer(read_only=True, required=False, allow_null=True)
    loans = MainLoansSerializer(read_only=True, required=False, allow_null=True)
    class Meta:
        model = Passives
        fields = '__all__'


class PassiveExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('id', 'property', 'transport', 'loan', 'funds', 'created_at')


PropertySerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
LoansSerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
