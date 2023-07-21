from rest_framework import serializers

from .models import Car


# Serializers
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
