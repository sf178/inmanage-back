from rest_framework import mixins, generics
from .models import *
from .serializers import *


class ExpenseCategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpensePersonalCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
