from rest_framework import serializers
from .models import *
from test_backend.custom_methods import CustomDateTimeField
from category.serializers import *


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Card
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    card_list = CardSerializer(many=True, read_only=True, required=False)
    # favourite_cards = CardSerializer(many=True, required=False)
    favourite_cards = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Card.objects.all(),
        required=False
    )
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Balance
        fields = '__all__'

    def update(self, instance, validated_data):
        # Get the list of card IDs from the request data
        card_ids = validated_data.get('card_list', [])
        # favourite_cards_data = validated_data.get('favourite_cards', [])
        # if favourite_cards_data is not None:
        #     instance.favourite_cards.set(favourite_cards_data)

        # Add the new card IDs to the existing card_list
        instance.card_list.add(*card_ids)

        # Update the remaining fields as usual
        instance.total = validated_data.get('total', instance.total)
        instance.total_in_currency = validated_data.get('total_in_currency', instance.total_in_currency)
        instance.total_income = validated_data.get('total_income', instance.total_income)
        instance.total_expenses = validated_data.get('total_expenses', instance.total_expenses)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.save()

        return instance


class BalanceIncomeSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(required=False)

    class Meta:
        model = Income
        fields = '__all__'


class BalanceExpensesSerializer(serializers.ModelSerializer):
    # category = PersonalExpenseCategorySerializer(required=False, read_only=True)
    created_at = CustomDateTimeField(required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=PersonalCategory.objects.all(),
        write_only=True, required=False
    )

    class Meta:
        model = Expenses
        fields = '__all__'
        # Поле 'category' теперь доступно только для записи
        extra_kwargs = {
            'category': {'write_only': True},
        }

    def to_representation(self, instance):
        """ Изменяем представление данных при сериализации. """
        representation = super().to_representation(instance)
        # Добавляем полное представление категории
        representation['category'] = PersonalExpenseCategorySerializer(instance.category).data
        return representation


CardSerializer._declared_fields['income'] = BalanceIncomeSerializer(many=True, read_only=True, required=False, allow_null=True)
CardSerializer._declared_fields['expenses'] = BalanceExpensesSerializer(many=True, read_only=True, required=False, allow_null=True)
