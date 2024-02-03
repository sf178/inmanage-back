from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from balance.models import Card
from balance.serializers import BalanceIncomeSerializer as IncomeSerializer
from test_backend.custom_methods import IsAuthenticatedCustom
from rest_framework import mixins, generics, status
from .models import WorkIncome, Work
from .serializers import *
from rest_framework.exceptions import ValidationError


class WorkIncomeListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = WorkIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return WorkIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     work_data = self.request.data.get('work')
    #     writeoff_account_id = self.request.data.get('writeoff_account')
    #     funds = self.request.data.get('funds')
    #     comment = self.request.data.get('comment')
    #
    #     # Создание или получение объекта Work
    #     if isinstance(work_data, dict):
    #         # Создание новой работы
    #         work_serializer = WorkSerializer(data=work_data)
    #         if work_serializer.is_valid(raise_exception=True):
    #             work = work_serializer.save(user=self.request.user)
    #         else:
    #             raise ValidationError(work_serializer.errors)
    #     else:
    #         # Получение существующей работы
    #         work = Work.objects.get(id=work_data, user=self.request.user)
    #
    #     # Создание объекта WorkIncome
    #     work_income = serializer.save(user=self.request.user, work=work)
    #
    #     # Добавление WorkIncome к списку доходов работы
    #     work.income.add(work_income)
    #
    #     # Создание связанного объекта Income
    #     if writeoff_account_id is not None:
    #         writeoff_account = Card.objects.get(id=writeoff_account_id, user=self.request.user)
    #         content_type = ContentType.objects.get_for_model(WorkIncome)
    #         income_data = {
    #             'user': self.request.user,
    #             'writeoff_account': writeoff_account,
    #             'funds': funds,
    #             'comment': comment,
    #             'content_type': content_type,
    #             'object_id': work_income.id
    #         }
    #         income_serializer = IncomeSerializer(data=income_data)
    #         if income_serializer.is_valid(raise_exception=True):
    #             income = income_serializer.save()
    #             work_income.child = income
    #             work_income.save()
    #         else:
    #             raise ValidationError(income_serializer.errors)

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        return self.create(self, request, *args, **kwargs)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WorkIncomeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = WorkIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return WorkIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class WorkIncomeCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
#     serializer_class = WorkIncomeSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#


class WorkListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)
        # headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticatedCustom]


    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class ProjectListView(mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#
#     def get_queryset(self):
#         return Project.objects.filter(user=self.request.user)
#
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# class ProjectDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticatedCustom]
#
#     def get_queryset(self):
#         return Project.objects.filter(user=self.request.user)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
