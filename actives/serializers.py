from rest_framework import serializers
from .models import *
from actives_deposit.models import *
from actives_deposit.serializers import *
from passives import serializers as pas
from inventory import serializers as inv
from test_backend.custom_methods import CustomDateTimeField
import json


def serialize_object_to_json(obj):
    return json.dumps(obj, default=str)


class JewelrySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Jewelry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.purchase_cost = validated_data.get('purchase_cost', instance.purchase_cost)
        instance.estimated_cost = validated_data.get('estimated_cost', instance.estimated_cost)
        instance.comment = validated_data.get('comment', instance.comment)
        if 'photo' in validated_data:
            instance.photo.delete(save=False)  # Удалить старое изображение, не сохраняя объект
            instance.photo = validated_data.get('photo')
        instance.save()
        return instance

    class Meta:
        model = Jewelry
        fields = '__all__'


class SecuritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Securities
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)
    equipment = inv.InventorySerializer(many=False, required=False)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Property
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.owner = validated_data.get('owner', instance.owner)
    #     instance.actual_price = validated_data.get('actual_price', instance.actual_price)
    #     instance.bought_price = validated_data.get('bought_price', instance.bought_price)
    #     instance.initial_payment = validated_data.get('initial_payment', instance.initial_payment)
    #     instance.loan_term = validated_data.get('loan_term', instance.loan_term)
    #     instance.rent_type = validated_data.get('rent_type', instance.rent_type)
    #     instance.percentage = validated_data.get('percentage', instance.percentage)
    #     instance.month_payment = validated_data.get('month_payment', instance.month_payment)
    #     instance.revenue = validated_data.get('revenue', instance.revenue)
    #     instance.equipment_price = validated_data.get('equipment_price', instance.equipment_price)
    #     instance.month_income = validated_data.get('month_income', instance.month_income)
    #     instance.month_expense = validated_data.get('month_expense', instance.month_expense)
    #     try:
    #         instance.average_profit = instance.month_income - instance.month_expense - instance.month_payment
    #     except:
    #         instance.average_profit = 0
    #     instance.save()
    #     return instance


class TransportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportImage
        fields = ('image',)


class TransportSerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)
    created_at = CustomDateTimeField(required=False)
    images = TransportImageSerializer(many=True, required=False)

    class Meta:
        model = Transport
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        transport = Transport.objects.create(**validated_data)
        if images_data:
            for image_data in images_data:
                TransportImage.objects.create(transport=transport, **image_data)
        return transport

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        # Обновите поля instance здесь
        if images_data:
            instance.images.all().delete()  # Перед добавлением новых изображений удаляем старые
            for image_data in images_data:
                TransportImage.objects.create(transport=instance, **image_data)
        return super().update(instance, validated_data)


class BusinessSerializer(serializers.ModelSerializer):
    loan_link = pas.LoansSerializer(many=False, required=False)
    equipment = inv.InventorySerializer(many=False, required=False)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Business
        fields = '__all__'


class ActivesIncomeSerializer(serializers.ModelSerializer):
    # property = PropertySerializer(required=False, allow_null=True)
    # transport = TransportSerializer(required=False, allow_null=True)
    # business = BusinessSerializer(required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = ActivesIncome
        fields = '__all__'


class ActivesExpensesSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = ActivesExpenses
        fields = '__all__'


class MainPropertySerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainProperties
        fields = '__all__'


class MainBusinessesSerializer(serializers.ModelSerializer):
    businesses = BusinessSerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainBusinesses
        fields = '__all__'


class MainTransportSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainTransport
        fields = '__all__'


class MainJewelriesSerializer(serializers.ModelSerializer):
    jewelries = JewelrySerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainJewelry
        fields = '__all__'


class MainSecuritiesSerializer(serializers.ModelSerializer):
    securities = SecuritiesSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainSecurities
        fields = '__all__'


# class MainLoansSerializer(serializers.ModelSerializer):
#     loans = ActivesLoansSerializer(many=True, read_only=True)
#     created_at = CustomDateTimeField(required=False)
#
#     class Meta:
#         model = MainLoans
#         fields = '__all__'


class MainDepositsSerializer(serializers.ModelSerializer):
    deposits = ActivesDepositsSerializer(many=True, read_only=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainDeposits
        fields = '__all__'


class ActivesSerializer(serializers.ModelSerializer):
    properties = MainPropertySerializer(read_only=True, required=False, allow_null=True)
    transports = MainTransportSerializer(read_only=True, required=False, allow_null=True)
    businesses = MainBusinessesSerializer(read_only=True, required=False, allow_null=True)
    jewelries = MainJewelriesSerializer(read_only=True, required=False, allow_null=True)
    securities = MainSecuritiesSerializer(read_only=True, required=False, allow_null=True)
    # loans = MainLoansSerializer(read_only=True, required=False, allow_null=True)
    deposits = MainDepositsSerializer(read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Actives
        fields = '__all__'


PropertySerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
PropertySerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
BusinessSerializer._declared_fields['income'] = ActivesIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
BusinessSerializer._declared_fields['expenses'] = ActivesExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)

