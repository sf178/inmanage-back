import os
from django.utils.deconstruct import deconstructible
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.timezone import now
from uuid import uuid4


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # Генерация уникального имени файла
        filename = '{}.{}'.format(uuid4().hex, ext)
        # Возвращение пути с новым именем файла
        return self.path + filename


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        from front.views import decodeJWT

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return False

        user = decodeJWT(auth_header)
        if not user:
            return False

        request.user = user
        if request.user and request.user.is_authenticated:
            from front.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False


class IsAuthenticatedOrReadCustom(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            from front.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return response

    exc_list = str(exc).split("DETAIL: ")

    return Response({"error": exc_list[-1]}, status=403)


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Форматирование даты и времени до миллисекунд и убрать лишние 0
        formatted_date_time = value.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
        return formatted_date_time