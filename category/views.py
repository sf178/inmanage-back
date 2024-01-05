from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import *
from .serializers import *
from rest_framework import generics, permissions, mixins
from test_backend.custom_methods import IsAuthenticatedCustom
from django.db.models import Q


# PersonalExpenseCategory Views
class PersonalExpenseCategoryListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PersonalExpenseCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return PersonalCategory.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalExpenseCategoryDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = PersonalExpenseCategorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return PersonalCategory.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class AssetCategoryListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = ActivesCategory.objects.all()
#     serializer_class = AssetCategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class AssetCategoryDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = ActivesCategory.objects.all()
#     serializer_class = AssetCategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
# # LiabilityCategory Views
# class LiabilityCategoryListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = PassivesCategory.objects.all()
#     serializer_class = LiabilityCategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class LiabilityCategoryDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = PassivesCategory.objects.all()
#     serializer_class = LiabilityCategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
# class ExpenseGeneralCategoryListView(mixins.ListModelMixin,
#                                      mixins.CreateModelMixin,
#                                      mixins.UpdateModelMixin,
#                                      generics.GenericAPIView):
#     serializer_class = ExpenseGeneralCategorySerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ExpenseGeneralCategory.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def perform_update(self, serializer):
#         instance = self.get_object()
#         if 'subcategories' in serializer.validated_data:
#             for subcat_name in serializer.validated_data.pop('subcategories'):
#                 # добавьте код для создания/обновления подкатегории
#                 ExpenseSubCategory.objects.update_or_create(name=subcat_name, general_category=instance)
#         serializer.save()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class ExpenseGeneralCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
#     serializer_class = ExpenseGeneralCategorySerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ExpenseGeneralCategory.objects.filter(user=self.request.user)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#
# class ExpenseGeneralSubcategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
#     serializer_class = ExpenseGeneralSubcategorySerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ExpenseSubCategory.objects.all()
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
