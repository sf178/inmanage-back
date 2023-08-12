from rest_framework import mixins, generics
from .models import ExpenseCategory
from .serializers import ExpenseCategorySerializer


class ExpenseCategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
