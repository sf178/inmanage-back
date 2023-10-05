from rest_framework import generics, permissions, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import get_object_or_404
from .models import *
import passives.models as pas
import inventory.models as inv
from .serializers import *
from сars_parser.parser.main import get_average
from .actives_scripts.transport_mark_model.main import set_mark_model
'''
####


            to change auth permissions you should change all rows:
                                
                                permission_classes = [permissions.IsAuthenticated]
                                
                                        to
                                        
                                permission_classes = [permissions.IsAuthenticated]        

            to enable check for user's id from request with object's id you should uncomment all sections:
            
                            if request.user.id != instance.user_id:
                                return Response({'error': 'You are not authorized to perform this operation.'},
                                                status=status.HTTP_401_UNAUTHORIZED)
                                                

####
'''

'''
####

        дописать функции для переноса объектов "в кредит" в passives/Loans

####
'''


class PropertyListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin,
                       mixins.CreateModelMixin):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # field to lookup object by

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.validated_data['actual_price'] = serializer.validated_data['bought_price']

        # Создание объекта Property
        self.perform_create(serializer)

        # Получение ID только что созданного объекта Property
        property_id = serializer.instance.id

        actives_content_type = ContentType.objects.get_for_model(Actives)

        # Создание нового объекта Inventory, используя ID объекта Property
        new_inventory = inv.Inventory.objects.create(
            user=serializer.validated_data['user'],
            content_type=actives_content_type,  # Здесь устанавливаем значение для category_object
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


class PropertyUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    serializer_class = PropertySerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        income_instances = []
        expenses_instances = []

        if 'incomes' in request.data:
            income_data = request.data.pop('incomes')
            for income in income_data:
                income_serializer = ActivesIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user=instance.user, property=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ActivesExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user=instance.user, property=instance)
                expenses_instances.append(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if income_instances:
            instance.income.add(*[income.id for income in income_instances])

        if expenses_instances:
            instance.expenses.add(*[expense.id for expense in expenses_instances])

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TransportListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TransportSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Transport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data['actual_price'] = serializer.validated_data['bought_price']

        # brand = request.data['mark']
        # name = request.data['model']

        # mark, model = set_mark_model(brand, name)
        # serializer.validated_data['mark'] = brand
        # serializer.validated_data['model'] = name
        # average_market, min_market, max_market = get_average(mark, model)
        # serializer.validated_data['average_market_price'] = average_market
        # serializer.validated_data['min_market_price'] = min_market
        # serializer.validated_data['max_market_price'] = max_market


        # Check if an object with the same name already exists
        # if Transport.objects.filter(name=name).exists():
        #     return Response({'message': 'Object with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Property object
        self.perform_create(serializer)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)

        # if serializer.instance.loan:
        #     # Create the Loans object
        #     loan = Loans(
        #         user_id=serializer.instance.user_id,
        #         name=serializer.instance.name,
        #         remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
        #         sum=serializer.instance.bought_price,
        #         loan_term=serializer.instance.loan_term,
        #         percentage=serializer.instance.percentage,
        #         month_payment=serializer.instance.month_payment,
        #         maintenance_cost=serializer.instance.month_expense
        #     )
        #     loan.save()
        #     serializer.instance.loan_link = loan
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class TransportUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = TransportSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        income_instances = []
        expenses_instances = []

        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = ActivesIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=instance.user, transport=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ActivesExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user, transport=instance)
                expenses_instances.append(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if income_instances:
            instance.income.add(*[income.id for income in income_instances])

        if expenses_instances:
            instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
        # instance = self.get_object()
        #
        # '''# Check if the user has the right to perform the update operation
        # if request.user.id != instance.user_id:
        #     return Response({'error': 'You are not authorized to perform this operation.'},
        #                     status=status.HTTP_401_UNAUTHORIZED)'''
        #
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        # return Response(serializer.data)


class TransportDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = TransportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transport.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BusinessListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        # name = request.data.get('name')
        # if Business.objects.filter(name=name).exists():
        #     return Response({'message': 'Object with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['actual_price'] = serializer.validated_data['bought_price']

        # Создание объекта Business
        self.perform_create(serializer)

        # Получение ID только что созданного объекта Business
        business_id = serializer.instance.id

        actives_content_type = ContentType.objects.get_for_model(Actives)

        # Создание нового объекта Inventory, используя ID объекта Business
        new_inventory = inv.Inventory.objects.create(
            user=serializer.validated_data['user'],
            content_type=actives_content_type,  # Здесь устанавливаем значение для category_object
            object_id=business_id,  # Здесь устанавливаем значение для object_id
            launch_status=False
        )

        # Обновление поля equipment в объекте Property
        property_instance = serializer.instance
        property_instance.equipment = new_inventory
        property_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # Check if the Property object has a non-empty loan field
        # if serializer.instance.loan:
        #     # Create the Loans object
        #     loan = Loans(
        #         user_id=serializer.instance.user_id,
        #         name=serializer.instance.name,
        #         #remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
        #         sum=serializer.instance.bought_price,
        #         loan_term=serializer.instance.loan_term,
        #         percentage=serializer.instance.percentage,
        #         month_payment=serializer.instance.month_payment,
        #         maintenance_cost=serializer.instance.month_expense
        #     )
        #     loan.save()
        #     serializer.instance.loan_link = loan
        # serializer.save()
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class BusinessUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        income_instances = []
        expenses_instances = []

        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = ActivesIncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=instance.user, business=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ActivesExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=instance.user, business=instance)
                expenses_instances.append(expenses_instance)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if income_instances:
            instance.income.add(*[income.id for income in income_instances])

        if expenses_instances:
            instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
        # instance = self.get_object()
        #
        # '''# Check if the user has the right to perform the update operation
        # if request.user.id != instance.user_id:
        #     return Response({'error': 'You are not authorized to perform this operation.'},
        #                     status=status.HTTP_401_UNAUTHORIZED)'''
        #
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        # return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        business_instance = self.get_object()
        inventory = business_instance.equipment
        if not inventory:
            if inventory.launch_status:
                inventory.launch_status = not inventory.launch_status
                inventory.save()
                business_instance.save(update_fields=['equipment'])
                serializer = PropertySerializer(business_instance)
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

                business_instance.save()

            serializer = PropertySerializer(business_instance)
            return Response(serializer.data)
        # if business_instance.equipment and business_instance.equipment.launch_status:
        #     business_instance.equipment.launch_status = not business_instance.equipment.launch_status
        #     business_instance.save(update_fields=['equipment'])
        #     business_instance = self.get_object()
        #
        #     serializer = PropertySerializer(business_instance)
        #     return Response(serializer.data)
        # # Если уже существует Inventory с launch_status равным False
        # if business_instance.equipment and not business_instance.equipment.launch_status:
        #     new_inventory = business_instance.equipment
        #
        #     # Получение ContentType для модели Actives
        #     actives_content_type = ContentType.objects.get_for_model(Actives)
        #
        #     # Создание нового объекта Inventory, наследующего поля старого
        #     # Создаем объект PreviousInventory на основе текущего состояния old_inventory
        #     previous_inv = inv.PreviousInventory.objects.create(
        #         user=new_inventory.user,
        #         content_type=new_inventory.content_type,
        #         object_id=new_inventory.object_id,
        #         launch_status=new_inventory.launch_status,
        #         total_cost=new_inventory.total_cost
        #     )
        #
        #     # Копируем связанные данные (assets и expenses)
        #     for asset in new_inventory.assets.all():
        #         previous_inv.assets.add(asset)
        #     for expense in new_inventory.expenses.all():
        #         previous_inv.expenses.add(expense)
        #     if new_inventory.previous_inventories.exists():
        #         last_previous_inventory = new_inventory.previous_inventories.latest('created_at')
        #         previous_inv.previous_inventory.set([last_previous_inventory])
        #         previous_inv.save()
        #     # Связывание старого объекта Inventory с новым через GenericRelation
        #     new_inventory.previous_inventories.add(previous_inv)
        #
        #     # Обновление поля equipment в Property
        #     business_instance.equipment = new_inventory
        #     business_instance.save()
        #
        #     business_instance = self.get_object()
        #
        #     # Сериализация объекта Property
        #     serializer = PropertySerializer(business_instance)
        #     return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

class BusinessDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IncomeListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = ActivesIncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivesIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id

        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Income object
class IncomeDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ActivesIncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivesIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = ActivesExpensesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivesExpenses.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id

        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ActivesExpensesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivesExpenses.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ActiveList(generics.ListAPIView):
    serializer_class = ActivesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Actives.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # user = request.data.pop('user', None)
        # actives = Actives.objects.get(user=user)
        # total_funds = 0
        # total_income = 0
        # total_expenses = 0
        # if actives.properties:
        #     total_funds += actives.properties.total_funds or 0
        #     total_income += actives.properties.total_income or 0
        #     total_expenses += actives.properties.total_expenses or 0
        # if actives.transports:
        #     total_funds += actives.transports.total_funds or 0
        #     total_income += actives.transports.total_income or 0
        #     total_expenses += actives.transports.total_expenses or 0
        # if actives.businesses:
        #     total_funds += actives.businesses.total_funds or 0
        #     total_income += actives.businesses.total_income or 0
        #     total_expenses += actives.businesses.total_expenses or 0
        #
        # # Сохранение обновленного объекта Actives
        # actives.total_funds = total_funds
        # actives.total_income = total_income
        # actives.total_expenses = total_expenses
        # actives.save()  # update_fields=['total_funds', 'total_income', 'total_expenses']

        instance = self.get_queryset().first()  # Note: This only returns the first active for the user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


