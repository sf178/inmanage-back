from rest_framework import generics, permissions, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib.contenttypes.models import ContentType
import inventory.models as inv

from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from сars_parser.parser.main import get_average
from .passives_scripts.transport_mark_model.main import set_mark_model


class LoansListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Loans.objects.all()
    serializer_class = LoansSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoansUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Loans.objects.all()
    serializer_class = LoansSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, loan=instance)
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
    queryset = Loans.objects.all()
    serializer_class = LoansSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PropertyListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin,
                       mixins.CreateModelMixin):
    queryset = Property.objects.filter(user_id='1')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

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
            user=serializer.validated_data['user'],
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


class PropertyUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, property=instance)
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

        # Если уже существует Inventory с launch_status равным False
        if property_instance.equipment and not property_instance.equipment.launch_status:
            old_inventory = property_instance.equipment

            # Получение ContentType для модели Actives
            actives_content_type = ContentType.objects.get_for_model(Passives)

            # Создание нового объекта Inventory, наследующего поля старого
            new_inventory = inv.Inventory.objects.create(
                user=old_inventory.user,
                content_type=actives_content_type,  # Здесь устанавливаем значение для category_object
                object_id=property_instance.id,  # Здесь устанавливаем значение для object_id
                launch_status=True
            )

            # Связывание старого объекта Inventory с новым через GenericRelation
            new_inventory.previous_inventories.set([old_inventory])

            # Обновление поля equipment в Property
            property_instance.equipment = new_inventory
            property_instance.save()

            # Сериализация объекта Property
            serializer = PropertySerializer(property_instance)
            return Response(serializer.data)

        if property_instance.equipment and property_instance.equipment.launch_status:
            property_instance.equipment.launch_status = not property_instance.equipment.launch_status
            property_instance.save(update_fields=['equipment'])
            serializer = PropertySerializer(property_instance)
            return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class PropertyDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Property.objects.filter(user_id='1')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TransportListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [permissions.AllowAny]

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


class TransportUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # expenses_instances = []

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = PassiveExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, transport=instance)
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
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PassivesListView(generics.ListAPIView):
    queryset = Passives.objects.all()
    serializer_class = PassivesSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = 1
        instance = Passives.objects.filter(user=user).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return self.list(request, *args, **kwargs)
    # permission_classes = [permissions.IsAuthenticated]
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
    queryset = Expenses.objects.all()
    serializer_class = PassiveExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = PassiveExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)