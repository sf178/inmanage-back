from rest_framework import serializers
from .models import Card, Balance


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    card_list = CardSerializer(many=True)
    class Meta:
        model = Balance
        fields = '__all__'

    def update(self, instance, validated_data):
        # Get the list of card IDs from the request data
        card_ids = validated_data.get('card_list', [])

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