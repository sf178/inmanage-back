from rest_framework import generics, permissions, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib.contenttypes.models import ContentType
import inventory.models as inv
from test_backend.custom_methods import IsAuthenticatedCustom

from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from сars_parser.parser.main import get_average
from .passives_scripts.transport_mark_model.main import set_mark_model


class LoansListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = LoansSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Loans.objects.filter(user=self.request.user)

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

class LoansUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = LoansSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Loans.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user.id, loan=instance)
                instance.expenses.add(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        #
        # if expenses_instances:
        #     instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class LoansDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = LoansSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Loans.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PropertyListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin,
                       mixins.CreateModelMixin):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['actual_price'] = serializer.validated_data['bought_price']

        # Создание объекта Property
        self.perform_create(serializer)

        # Получение ID только что созданного объекта Property
        property_id = serializer.instance.id

        passives_content_type = ContentType.objects.get_for_model(Passives)

        # Создание нового объекта Inventory, используя ID объекта Property
        new_inventory = inv.Inventory.objects.create(
            user=serializer.instance.user,
            content_type=passives_content_type,  # Здесь устанавливаем значение для category_object
            object_id=property_id,  # Здесь устанавливаем значение для object_id
            launch_status=False
        )

        # Обновление поля equipment в объекте Property
        property_instance = serializer.instance
        property_instance.equipment = new_inventory
        property_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)

class PropertyUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedCustom]

    lookup_field = 'id'
    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user.id, property=instance)
                instance.expenses.add(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        #
        # if expenses_instances:
        #     instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        property_instance = self.get_object()
        inventory = property_instance.equipment

        if inventory:
            if not inventory.launch_status:
                inventory.launch_status = not inventory.launch_status
                inventory.save()
                property_instance.save(update_fields=['equipment'])
                serializer = PropertySerializer(property_instance)
                return Response(serializer.data)

            # Если уже существует Inventory с launch_status равным False
            elif inventory.launch_status:
                inventory.launch_status = False
                # inventory.save()

                # Создание объекта PreviousInventory на основе текущего состояния inventory
                previous_inv = inv.PreviousInventory.objects.create(
                    user=inventory.user,
                    content_type=inventory.content_type,
                    object_id=inventory.object_id,
                    launch_status=False,
                    total_cost=inventory.total_cost
                )
                # Копирование связанных assets и expenses
                try:
                    for asset in inventory.assets.all():
                        prev_asset = inv.PreviousInventoryAsset.objects.create(
                            user=asset.user,
                            text=asset.text,
                            added=asset.added,
                            price=asset.price,
                            flag=asset.flag
                        )
                        previous_inv.assets.add(prev_asset)
                except:
                    pass
                try:
                    for expense in inventory.expenses.all():
                        previous_inv.expenses.add(expense)
                except:
                    pass

                # Связь с предыдущим инвентарем
                if inventory.previous_inventories.exists():
                    last_previous_inventory = inventory.previous_inventories.latest('created_at')
                    previous_inv.previous_inventory.set([last_previous_inventory])
                    previous_inv.save()

                # Добавляем созданный объект PreviousInventory в поле previous_inventories текущего inventory
                inventory.previous_inventories.add(previous_inv)
                inventory.save()  # Удостоверимся, что изменения сохранены

                property_instance.save()

            serializer = PropertySerializer(property_instance)
            return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class PropertyDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TransportListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TransportSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Transport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data['actual_price'] = serializer.validated_data['bought_price']

        # brand = request.data['mark']
        # name = request.data['model']

        # mark, model = set_mark_model(brand, name)

        # serializer.mark = brand
        # serializer.model = name
        #
        # serializer.validated_data['mark'] = brand
        # serializer.validated_data['model'] = name
        # average_market, min_market, max_market = get_average(mark, model)
        # serializer.average_market_price = average_market
        # serializer.min_market_price = min_market
        # serializer.max_market_price = max_market

        # serializer.validated_data['average_market_price'] = average_market
        # serializer.validated_data['min_market_price'] = min_market
        # serializer.validated_data['max_market_price'] = max_market

        # Create the Property object
        self.perform_create(serializer)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Проверка на наличие 'user' в data перед сохранением
        # Если 'user' уже присутствует, это может означать попытку инъекции данных, и следует вернуть ошибку
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)

class TransportUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = TransportSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Transport.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user.id, transport=instance)
                instance.expenses.add(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        #
        # if expenses_instances:
        #     instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class TransportDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = TransportSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Transport.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PassivesListView(generics.ListAPIView):
    serializer_class = PassivesSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Passives.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        user = request.user.id

        instance = Passives.objects.filter(user=user).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return self.list(request, *args, **kwargs)
    # permission_classes = [IsAuthenticatedCustom]
    # def calculate_totals(self, user_id):
    #     # Retrieve related MainProperties, MainTransport, and MainLoans if they exist
    #     properties = MainProperties.objects.filter(user_id=user_id).first()
    #     transports = MainTransport.objects.filter(user_id=user_id).first()
    #     loans = MainLoans.objects.filter(user_id=user_id).first()
    #
    #     # Calculate the total funds and expenses from the related objects
    #     total_funds = sum([obj.total_funds for obj in [properties, transports, loans] if obj])
    #     total_expenses = sum([obj.total_expenses for obj in [properties, transports, loans] if obj])
    #
    #     return total_funds, total_expenses
    #
    # def get(self, request, *args, **kwargs):
    #     user_id = 1
    #     passives, created = Passives.objects.get_or_create(user_id=user_id)
    #
    #     # Calculate the total funds and expenses from related objects
    #     total_funds, total_expenses = self.calculate_totals(user_id)
    #
    #     # Update the Passives object with the calculated totals
    #     passives.total_funds = total_funds
    #     passives.total_expenses = total_expenses
    #     passives.properties = MainProperties.objects.filter(user_id=user_id).first()
    #     passives.transports = MainTransport.objects.filter(user_id=user_id).first()
    #     passives.loans = MainLoans.objects.filter(user_id=user_id).first()
    #     passives.save()
    #
    #     # Return the serialized Passives object
    #     serializer = self.get_serializer(passives)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = PassiveExpensesSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user)

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

# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = PassiveExpensesSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)