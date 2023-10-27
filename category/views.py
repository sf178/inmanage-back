from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError

from .models import *
from .serializers import *
from rest_framework import generics, permissions, mixins
from test_backend.custom_methods import IsAuthenticatedCustom
from django.db.models import Q


class ExpensePersonalCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ExpensePersonalCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpensePersonalCategory.objects.filter(Q(user=self.request.user) | Q(is_default=True))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")


class ExpensePersonalCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpensePersonalCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpensePersonalCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExpenseGeneralCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.filter(Q(user=self.request.user) | Q(is_default=True))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")


class ExpenseGeneralCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)