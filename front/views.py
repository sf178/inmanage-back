import jwt as jwtlib
import os
from rest_framework import status
from cryptography.fernet import Fernet, InvalidToken
import environ

from .models import Jwt, CustomUser, Favorite, TemporaryCustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, RegisterSerializer, RefreshSerializer, UserProfileSerializer, UserProfile, FavoriteSerializer,
    CustomUserSerializer
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .auth import Authentication
from test_backend.custom_methods import IsAuthenticatedCustom
from rest_framework.viewsets import ModelViewSet
import re
from django.db.models import Q, Count, Subquery, OuterRef
from balance.models import Balance
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializer

env = environ.Env()

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwtlib.encode(
        #{"exp": datetime.now() + timedelta(minutes=5), **payload},
        {"exp": datetime.now() + timedelta(days=365), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token():
    return jwtlib.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]
    decoded = jwtlib.decode(token, algorithms=['HS256'], key=settings.SECRET_KEY)
    if decoded:
        try:
            return CustomUser.objects.get(id=decoded["user_id"])
        except Exception:
            return None


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Аутентификация с использованием номера телефона
        user = authenticate(
            phone_number=serializer.validated_data['phone_number'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid phone number or password"}, status="400")

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id=user.id, access=access, refresh=refresh
        )

        return Response({"access": access, "refresh": refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.pop("phone_number")
        temp_token = str(phone_number)[-4:]  # последние 4 цифры номера телефона

        # Шифрование пароля
        cipher = Fernet(env('SECRET_CRYPTO_KEY'))
        # cipher = Fernet(b'gBLgsatgAHXe1i0Ckx5ylXpWWORpRtX3-MOM6VV3J5w=')
        encrypted_password = cipher.encrypt(serializer.validated_data["password"].encode())
        serializer.validated_data["password"] = encrypted_password

        # Закомментированный код для отправки смс
        # send_sms(phone_number, "Your verification code is: 1111")

        # Создание объекта TemporaryCustomUser с temp_token
        TemporaryCustomUser.objects.create(phone_number=phone_number, temp_token=temp_token,
                                           **serializer.validated_data)

        return Response({"temp_token": temp_token, "message": "Verification code sent."},
                        status=status.HTTP_201_CREATED)


class ConfirmRegistrationView(APIView):
    def post(self, request):
        temp_token = request.data.get("temp_token")
        verification_code = request.data.get("code")

        if not temp_token or not verification_code:
            return Response({"error": "Missing required data."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка кода (пока просто 1111)
        if verification_code != "1111":
            return Response({"error": "Incorrect verification code."}, status=status.HTTP_400_BAD_REQUEST)

        # Получение объекта TemporaryCustomUser по temp_token
        try:
            temp_user = TemporaryCustomUser.objects.get(temp_token=temp_token)
        except TemporaryCustomUser.DoesNotExist:
            return Response({"error": "Invalid token or data expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Дешифровка пароля
        cipher = Fernet(env('SECRET_CRYPTO_KEY'))
        # cipher = Fernet(b'gBLgsatgAHXe1i0Ckx5ylXpWWORpRtX3-MOM6VV3J5w=')
        try:
            decrypted_password = cipher.decrypt(temp_user.password.tobytes()).decode()
        except InvalidToken:
            return Response({"error": "Failed to decrypt password."}, status=status.HTTP_400_BAD_REQUEST)
        # Создание объекта CustomUser на основе данных из TemporaryCustomUser
        user_data = {
            "phone_number": temp_user.phone_number,
            #"email": temp_user.email,
            # "password": temp_user.password,
            # "password": decrypted_password,
            "is_staff": temp_user.is_staff,
            "is_superuser": temp_user.is_superuser
            # добавьте здесь любые другие поля, если они есть
        }
        #if user_data["email"] is None:
        #    user_data["email"] = ""
        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.validated_data["password"] = decrypted_password

        # Создание объекта CustomUser
        created_user = CustomUser.objects.create_user(**user_serializer.validated_data)
        profile = UserProfile.objects.get(user=created_user)
        profile.name = temp_user.name
        profile.birthdate = temp_user.birthdate
        profile.save()
        # Удаление временного объекта пользователя
        temp_user.delete()

        return Response({"success": "User created."}, status=status.HTTP_201_CREATED)


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})


class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        if keyword:
            search_fields = (
                "user__username", "first_name", "last_name", "user__email"
            )
            query = self.get_query(keyword, search_fields)
            try:
                return self.queryset.filter(query).filter(**data).exclude(
                    Q(user_id=self.request.user.id) |
                    Q(user__is_superuser=True)
                ).annotate(
                    fav_count=Count(self.user_fav_query(self.request.user))
                ).order_by("-fav_count")
            except Exception as e:
                raise Exception(e)

        result = self.queryset.filter(**data).exclude(
            Q(user_id=self.request.user.id) |
            Q(user__is_superuser=True)
        ).annotate(
            fav_count=Count(self.user_fav_query(self.request.user))
        ).order_by("-fav_count")
        return result

    @staticmethod
    def user_fav_query(user):
        try:
            return user.user_favorites.favorite.filter(id=OuterRef("user_id")).values("pk")
        except Exception:
            return []


    @staticmethod
    def get_query(query_string, search_fields):
        query = None  # Query to search for every search term
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

class UserProfilePartialUpdateView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   generics.GenericAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return self.request.user.user_profile

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class MeView(APIView):
    permission_classes = (IsAuthenticatedCustom, )
    serializer_class = UserProfileSerializer

    def get(self, request):
        data = {}
        try:
            data = self.serializer_class(request.user.user_profile).data
        except Exception:
            data = {
                "user": {
                    "id": request.user.id
                }
            }
        return Response(data, status=200)


class LogoutView(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        user_id = request.user.id

        Jwt.objects.filter(user_id=user_id).delete()

        return Response("logged out successfully", status=200)
