from datetime import datetime

import pytz
from django.http import JsonResponse
from django.utils.timezone import make_aware, now
from rest_framework import generics, permissions, mixins
from django.db.models import Sum, Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import *
from .serializers import *
from test_backend.custom_methods import IsAuthenticatedCustom

from actives.models import Actives
from passives.models import Passives
from todo.models import Planner
from rest_framework import status
from rest_framework.response import Response
import requests
import json


class CurrencyListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if is_many:
            # Обработка списка объектов
            response_data = []
            for item_data in request.data:
                # Поиск или создание объекта по полю 'name'
                instance = Currency.objects.filter(name=item_data['name']).first()
                if instance:
                    # Если объект существует, обновляем его
                    serializer = self.get_serializer(instance, data=item_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    # Если объект не существует, создаем новый
                    serializer = self.get_serializer(data=item_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                response_data.append(serializer.data)
            headers = self.get_success_headers(response_data)
            return Response(response_data, status=status.HTTP_200_OK, headers=headers)
        else:
            # Обработка одиночного объекта (аналогично списку)
            instance = Currency.objects.filter(name=request.data['name']).first()
            if instance:
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class PaymentListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Payment Detail View
class PaymentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Payment Update (Patch) View
class PaymentUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PaymentDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CardListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Card.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)


class CardDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Card.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CardUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = CardSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Card.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = BalanceIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=instance.user.id, writeoff_account=instance)
                instance.income.add(income_instance)
        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = BalanceExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user.id, writeoff_account=instance)
                instance.expenses.add(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class CardDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Card.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BalanceListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Balance.objects.filter(user=self.request.user)

    '''тестовая хуйня, удалить если не сработает'''
    @staticmethod
    def calculate_totals(user, timezone='UTC'):
        user_timezone = pytz.timezone(timezone)
        today = now().astimezone(user_timezone)
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        total_funds = 0
        card_funds = 0
        daily_income = 0
        daily_expense = 0
        monthly_income = 0
        monthly_expense = 0

        # From Actives
        active = Actives.objects.filter(user=user).first()
        if active:
            total_funds += (active.total_funds or 0)

        # From Passives
        passive = Passives.objects.filter(user=user).first()
        if passive:
            total_funds += (passive.total_funds or 0)

        # From Cards
        cards = Card.objects.filter(user=user)
        for card in cards:
            card_funds += (card.remainder or 0)
            daily_income += card.income.filter(created_at__gte=start_of_day).aggregate(Sum('funds'))['funds__sum'] or 0
            daily_expense += card.expenses.filter(created_at__gte=start_of_day).aggregate(Sum('funds'))[
                                 'funds__sum'] or 0
            monthly_income += card.income.filter(created_at__gte=start_of_month).aggregate(Sum('funds'))[
                                  'funds__sum'] or 0
            monthly_expense += card.expenses.filter(created_at__gte=start_of_month).aggregate(Sum('funds'))[
                                   'funds__sum'] or 0
        card_income = sum(card.total_income or 0 for card in cards)
        card_expenses = sum(card.total_expense or 0 for card in cards)

        total_funds += card_funds

        return daily_income, daily_expense, monthly_income, monthly_expense, card_income, card_expenses, total_funds, card_funds
    '''ниже нормальная версия, использовать при неуспехе'''
    # @staticmethod
    # def calculate_totals(user):
    #     total_expenses = 0
    #     total_income = 0
    #     total_funds = 0
    #     card_funds = 0
    #     card_income = 0
    #     card_expenses = 0
    #     # From Actives
    #     active = Actives.objects.filter(user=user).first()
    #     if active:
    #         total_funds += (active.total_funds or 0)
    #         total_income += (active.total_income or 0)
    #         total_expenses += (active.total_expenses or 0)
    #
    #     # From Passives
    #     passive = Passives.objects.filter(user=user).first()
    #     if passive:
    #         total_funds += (passive.total_funds or 0)
    #         total_expenses += (passive.total_expenses or 0)
    #
    #     # From Cards
    #     cards = Card.objects.filter(user=user)
    #     for card in cards:
    #         card_expenses += (card.total_expense or 0)
    #         card_income += (card.total_income or 0)
    #         card_funds += (card.remainder or 0)
    #
    #     # From Planner
    #     planner = Planner.objects.filter(user=user).first()
    #     if planner:
    #         total_income += (planner.total_income or 0)
    #         total_expenses += (planner.total_expenses or 0)
    #     # total_income = card_income
    #     # total_expenses += card_expenses
    #     total_funds += (total_income + (card_funds - card_income)) - total_expenses
    #
    #     return total_income, total_expenses, total_funds, card_funds, card_income, card_expenses

    def get(self, request, *args, **kwargs):
        user_timezone_str = request.headers.get('Time-Zone', 'UTC')
        user = request.user
        balance, created = Balance.objects.get_or_create(user=user)

        daily_income, daily_expense, monthly_income, monthly_expense, card_income, card_expenses, total_funds, card_funds = self.calculate_totals(user, user_timezone_str)

        balance.daily_income = daily_income
        balance.daily_expense = daily_expense
        balance.monthly_income = monthly_income
        balance.monthly_expense = monthly_expense
        balance.total_income = card_income
        balance.total_expenses = card_expenses
        balance.total = total_funds
        balance.card_funds = card_funds
        balance.save()

        serializer = self.serializer_class(balance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        return self.perform_create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        balance = Balance.objects.filter(user=user).first()

        serializer = self.get_serializer(balance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # extract card data from request
        card_data = request.data.pop('card', None)
        favourite_cards_data = request.data.pop('favourite_cards', None)

        if card_data:
            card_serializer = CardSerializer(data=card_data)
            if card_serializer.is_valid():
                card = card_serializer.save(user=user, is_editable=True, is_deletable=True)  # save card instance
                balance.card_list.add(card)
            else:
                return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # handle favourite_cards data
        if favourite_cards_data:
            # return Response({"favourite_cards_data": favourite_cards_data})
            if isinstance(favourite_cards_data, list):
                # Очистить текущие избранные карты, если нужно
                balance.favourite_cards.clear()

                for card_id in favourite_cards_data:
                    try:
                        card_to_add = Card.objects.get(id=card_id)
                        balance.favourite_cards.add(card_to_add)
                    except Card.DoesNotExist:
                        return Response({"error": f"Card with id {card_id} does not exist."},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
               return Response({"error": "favourite_cards must be a list."},
                                status=status.HTTP_400_BAD_REQUEST)

        instance = Balance.objects.filter(user=user).first()
        inst_serializer = self.get_serializer(instance)

        return Response(inst_serializer.data)

    def perform_create(self, serializer, *args, **kwargs):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user, is_editable=True, is_deletable=True)
# class BalanceUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
#     queryset = Balance.objects.all()
#     serializer_class = BalanceSerializer
#     lookup_field = 'id'
#
#


class BalanceDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Balance.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IncomeListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = BalanceIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Income.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer, *args, **kwargs):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)


# View mixin for retrieving, updating, and deleting a specific Income object
class IncomeDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = BalanceIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Income.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = BalanceExpensesSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Expenses.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)


# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = BalanceExpensesSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return Expenses.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)