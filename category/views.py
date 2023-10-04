from rest_framework import mixins, generics
from .models import *
from .serializers import *


class ExpensePersonalCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ExpensePersonalCategory.objects.all()
    serializer_class = ExpensePersonalCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpensePersonalCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ExpensePersonalCategory.objects.all()
    serializer_class = ExpensePersonalCategorySerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExpenseGeneralCategoryListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ExpenseGeneralCategory.objects.all()
    serializer_class = ExpenseGeneralCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpenseGeneralCategoryDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ExpenseGeneralCategory.objects.all()
    serializer_class = ExpenseGeneralCategorySerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)