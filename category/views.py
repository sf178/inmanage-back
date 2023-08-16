from rest_framework import mixins, generics
from .models import *
from .serializers import *


class ExpensePersonalCategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpensePersonalCategory.objects.all()
    serializer_class = ExpensePersonalCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ExpenseGeneralCategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpenseGeneralCategory.objects.all()
    serializer_class = ExpenseGeneralCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)