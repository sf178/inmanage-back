from rest_framework import generics, permissions, mixins
from django.db.models import Sum, Q
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import *
from .serializers import *

from actives.models import Actives
from passives.models import Passives
from rest_framework import status
from rest_framework.response import Response


class CardListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CardDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CardUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = BalanceIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=1, card=instance)
                instance.income.add(income_instance)
        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = BalanceExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, card=instance)
                instance.expenses.add(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class CardDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BalanceListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.AllowAny]
    @staticmethod
    def calculate_totals(user):
        total_expenses = 0
        total_income = 0
        total_funds = 0
        card_funds = 0
        card_income = 0
        card_expenses = 0

        # From Actives
        active = Actives.objects.filter(user=user).first()
        if active:
            total_funds += (active.total_funds or 0)
            total_income += (active.total_income or 0)
            total_expenses += (active.total_expenses or 0)

        # From Passives
        passive = Passives.objects.filter(user=user).first()
        if passive:
            total_funds += (passive.total_funds or 0)
            total_expenses += (passive.total_expenses or 0)

        # From Cards
        cards = Card.objects.filter(user=user)
        for card in cards:
            card_expenses += (card.total_expense or 0)
            card_income += (card.total_income or 0)
            card_funds += (card.remainder or 0)

        total_income += card_income
        total_expenses += card_expenses
        total_funds += card_funds

        return total_income, total_expenses, total_funds, card_funds, card_income, card_expenses

    def get(self, request, *args, **kwargs):
        user = 1
        balance = Balance.objects.filter(user_id=user).first()  # or create a new one

        total_income, total_expenses, total, card_funds, card_income, card_expenses = self.calculate_totals(user=user)

        balance.total_income = total_income
        balance.total_expenses = total_expenses
        balance.total = total
        balance.card_funds = card_funds
        balance.card_income = card_income
        balance.card_expenses = card_expenses
        balance.save()

        serializer = self.get_serializer(balance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        user = 1
        balance = Balance.objects.filter(user_id=user).first()

        serializer = self.get_serializer(balance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # extract card data from request
        card_data = request.data.pop('card', None)

        if card_data:
            card_serializer = CardSerializer(data=card_data)
            if card_serializer.is_valid():
                card = card_serializer.save()  # save card instance
            else:
                return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            card = None

        # update card_list if card is not None
        if card is not None:
            balance.card_list.add(card)

        instance = Balance.objects.filter(user_id=user).first()
        inst_serializer = self.get_serializer(instance)

        return Response(inst_serializer.data)

# class BalanceUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
#     queryset = Balance.objects.all()
#     serializer_class = BalanceSerializer
#     lookup_field = 'id'
#
#


class BalanceDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IncomeListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = Income.objects.all()
    serializer_class = BalanceIncomeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Income object
class IncomeDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Income.objects.all()
    serializer_class = BalanceIncomeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = BalanceExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = BalanceExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)