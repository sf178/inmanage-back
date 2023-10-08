from rest_framework import serializers
from .models import UserProfile, CustomUser, Favorite, TemporaryCustomUser
from phonenumber_field.serializerfields import PhoneNumberField


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    #email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField()
    password = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    #email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        exclude = ("password",)

class TemporaryCustomUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    #email = serializers.EmailField(required=False)

    class Meta:
        model = TemporaryCustomUser
        exclude = ("password",)

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class FavoriteSerializer(serializers.Serializer):
    favorite_id = serializers.IntegerField()
