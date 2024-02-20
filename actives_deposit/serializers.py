from rest_framework import serializers
from .models import *


# class ActivesLoansSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivesLoans
#         fields = '__all__'
#

class ActivesDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivesDeposit
        fields = '__all__'