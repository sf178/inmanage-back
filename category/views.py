from rest_framework import mixins, generics
from .models import *
from .serializers import *
from rest_framework import generics, permissions, mixins


class ExpensePersonalCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ExpensePersonalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpensePersonalCategory.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpensePersonalCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpensePersonalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpensePersonalCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExpenseGeneralCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpenseGeneralCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ExpenseGeneralCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseGeneralCategory.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)