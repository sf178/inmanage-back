from rest_framework import generics, permissions, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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

    def perform_create(self, serializer):
        work_data = self.request.data.get('work')
        if isinstance(work_data, dict):
            # Создание новой работы, если предоставлен объект work с полем name.
            work_serializer = WorkSerializer(data=work_data)
            if work_serializer.is_valid(raise_exception=True):
                work = work_serializer.save(user=self.request.user)
                serializer.save(user=self.request.user, work=work)
                work.income.add(serializer.instance)  # Добавление в income для новой работы
            else:
                raise ValidationError(work_serializer.errors)
        else:
            # Привязка к существующему Work по id и добавление в income
            try:
                work = Work.objects.get(id=work_data, user=self.request.user)
            except Work.DoesNotExist:
                raise ValidationError("Work with the given ID does not exist")

            serializer.save(user=self.request.user, work=work)
            work.income.add(serializer.instance)  # Добавление в income для существующей работы

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
