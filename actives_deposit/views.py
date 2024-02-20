from rest_framework import mixins, generics

from test_backend.custom_methods import IsAuthenticatedCustom
from .models import ActivesDeposit
from actives.models import MainDeposits
from actives.serializers import ActivesIncomeSerializer, ActivesExpensesSerializer
from .serializers import ActivesDepositsSerializer
from rest_framework.response import Response


# Обработчик для получения списка и создания новых займов
# class ActivesLoansListView(mixins.ListModelMixin,
#                            mixins.CreateModelMixin,
#                            generics.GenericAPIView):
#     # queryset = ActivesLoans.objects.all()
#     serializer_class = ActivesLoansSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ActivesLoans.objects.filter(user=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         loan = serializer.save(user=self.request.user)
#         main_loan = MainLoans.objects.get(user=loan.user)
#         main_loan.loans.add(loan)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ActivesLoansDetailView(mixins.RetrieveModelMixin,
#                              generics.GenericAPIView):
#     # queryset = ActivesLoans.objects.all()
#     serializer_class = ActivesLoansSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ActivesLoans.objects.filter(user=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# # Обработчик для обновления займа
# class ActivesLoansUpdateView(mixins.UpdateModelMixin,
#                              generics.GenericAPIView):
#     # queryset = ActivesLoans.objects.all()
#     serializer_class = ActivesLoansSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ActivesLoans.objects.filter(user=self.request.user)
#
#     def patch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         # expenses_instances = []
#
#         if 'expenses' in request.data:
#             expenses_data = request.data.pop('expenses')
#             for expense in expenses_data:
#                 expenses_serializer = ActivesExpensesSerializer(data=expense)
#                 expenses_serializer.is_valid(raise_exception=True)
#                 expenses_instance = expenses_serializer.save(user_id=instance.user.id, loan=instance)
#                 instance.expenses.add(expenses_instance)
#
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         #
#         # if expenses_instances:
#         #     instance.expenses.add(*[expense.id for expense in expenses_instances])
#
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#
#         return Response(serializer.data)
#
#
# # Обработчик для удаления займа
# class ActivesLoansDeleteView(mixins.DestroyModelMixin,
#                              generics.GenericAPIView):
#     # queryset = ActivesLoans.objects.all()
#     serializer_class = ActivesLoansSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return ActivesLoans.objects.filter(user=self.request.user)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#

class ActivesDepositListView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    # queryset = ActivesDeposit.objects.all()
    serializer_class = ActivesDepositsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ActivesDeposit.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        deposit = serializer.save(user=self.request.user)
        main_deposit = MainDeposits.objects.get(user=deposit.user)
        main_deposit.deposits.add(deposit)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ActivesDepositDetailView(mixins.RetrieveModelMixin,
                               generics.GenericAPIView):
    # queryset = ActivesDeposit.objects.all()
    serializer_class = ActivesDepositsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ActivesDeposit.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Обработчик для обновления депозита
class ActivesDepositUpdateView(mixins.UpdateModelMixin,
                               generics.GenericAPIView):
    # queryset = ActivesDeposit.objects.all()
    serializer_class = ActivesDepositsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ActivesDeposit.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'incomes' in request.data:
            income_data = request.data.pop('incomes')
            for income in income_data:
                income_serializer = ActivesIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user=instance.user, property=instance)
                instance.income.add(income_instance)

        return self.partial_update(request, *args, **kwargs)


# Обработчик для удаления депозита
class ActivesDepositDeleteView(mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    # queryset = ActivesDeposit.objects.all()
    serializer_class = ActivesDepositsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return ActivesDeposit.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)