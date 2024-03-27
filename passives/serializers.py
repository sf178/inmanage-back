from rest_framework import serializers
from .models import *
from inventory import serializers as inv
from test_backend.custom_methods import CustomDateTimeField


class LoansSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Loans
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    loan_link = LoansSerializer(many=False, required=False)
    equipment = inv.InventorySerializer(many=False, required=False)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Property
        fields = '__all__'


class TransportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportImage
        fields = ('image',)


class TransportSerializer(serializers.ModelSerializer):
    loan_link = LoansSerializer(many=False, required=False)
    created_at = CustomDateTimeField(required=False)
    images = TransportImageSerializer(many=True, required=False)

    class Meta:
        model = Transport
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        transport = Transport.objects.create(**validated_data)
        for image in images:
            TransportImage.objects.create(transport=transport,
                                          image=image['image'])  # Предполагается, что 'image' - это файл
        return transport

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        # Обновите поля instance здесь
        if images_data:
            instance.images.all().delete()  # Перед добавлением новых изображений удаляем старые
            for image_data in images_data:
                TransportImage.objects.create(transport=instance, **image_data)
        return super().update(instance, validated_data)


class MainPropertiesSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainProperties
        fields = '__all__'


class MainLoansSerializer(serializers.ModelSerializer):
    loans = LoansSerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainLoans
        fields = '__all__'


class MainTransportSerializer(serializers.ModelSerializer):
    transport = TransportSerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainTransport
        fields = '__all__'


class MainBorrowsSerializer(serializers.ModelSerializer):
    borrows = LoansSerializer(many=True, read_only=True, required=False, allow_null=True)
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = MainBorrows
        fields = '__all__'


class PassivesSerializer(serializers.ModelSerializer):
    properties = MainPropertiesSerializer(read_only=True, required=False, allow_null=True)
    transports = MainTransportSerializer(read_only=True, required=False, allow_null=True)
    loans = MainLoansSerializer(read_only=True, required=False, allow_null=True)
    borrows = MainBorrowsSerializer(read_only=True, required=False, allow_null=True)

    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Passives
        fields = '__all__'


class PassiveExpensesSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Expenses
        fields = '__all__'


PropertySerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
TransportSerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
LoansSerializer._declared_fields['expenses'] = PassiveExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
