from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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
        data = request.data

        # Если передан список, обрабатываем каждую категорию в списке
        if isinstance(data, list):
            created_categories = []
            for category_data in data:
                serializer = self.get_serializer(data=category_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_categories.append(serializer.data)
            return Response(created_categories, status=201)

        # Если передана одна категория
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)

class ExpensePersonalCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpensePersonalCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpensePersonalCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExpenseGeneralCategoryListView(mixins.ListModelMixin,
                                     mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin,
                                     generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        if 'subcategories' in serializer.validated_data:
            for subcat_name in serializer.validated_data.pop('subcategories'):
                # добавьте код для создания/обновления подкатегории
                ExpenseSubCategory.objects.update_or_create(name=subcat_name, general_category=instance)
        serializer.save()


class ExpenseGeneralCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)