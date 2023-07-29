from rest_framework import generics, permissions, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.db.models import Sum

from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from сars_parser.parser.main import get_average
from .actives_scripts.transport_mark_model.main import set_mark_model
'''
####


            to change auth permissions you should change all rows:
                                
                                permission_classes = [permissions.AllowAny]
                                
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
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # field to lookup object by

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the Property object
        self.perform_create(serializer)

        # Check if the Property object has a non-empty loan field
        if serializer.instance.loan:
            # Create the Loans object
            loan = Loans(
                user_id=serializer.instance.user_id,
                name=serializer.instance.name,
                remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
                sum=serializer.instance.bought_price,
                loan_term=serializer.instance.loan_term,
                percentage=serializer.instance.percentage,
                month_payment=serializer.instance.month_payment,
                maintenance_cost=serializer.instance.month_expense
            )
            loan.save()
            serializer.instance.loan_link = loan
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class PropertyUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        income_instances = []
        expenses_instances = []

        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = IncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=1, property=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, property=instance)
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



class PropertyDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Property.objects.filter(user_id='1')
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PropertyAssetListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin,
                            mixins.CreateModelMixin):
    queryset = PropertyAsset.objects.all()
    serializer_class = PropertyAssetSerializer
    permission_classes = [AllowAny]

    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'property_id'  # field to lookup object by

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        queryset = PropertyAsset.objects.filter(property_id=property_id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PropertyAssetCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = PropertyAsset.objects.all()

    serializer_class = PropertyAssetSerializer
    permission_classes = [AllowAny]

    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # field to lookup object by

    def post(self, request, *args, **kwargs):
        '''address = request.data.get('address')
        if Property.objects.filter(address=address).exists():
            return Response({'message': 'Object with this address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        # return self.create(request, *args, **kwargs)
        '''

        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    '''def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)'''


class PropertyAssetUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = PropertyAsset.objects.all()
    serializer_class = PropertyAssetSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            obj_ids = []
            for obj in request.data:
                obj_ids.append(obj['id'])

            queryset = self.filter_queryset(self.get_queryset().filter(id__in=obj_ids))
            for item in queryset:
                for obj in request.data:
                    if item.id == obj['id']:
                        serializer = self.get_serializer(item, data=obj, partial=True)
                        serializer.is_valid(raise_exception=True)
                        self.perform_update(serializer)
                        continue
            return Response({'message': 'Objects updated successfully.'})
            # return Response()

        else:
            # If the request data is not a list, assume it is a single object and update it

            instance = self.get_object()
            ## '''# Check if the user has the right to perform the update operation
            ##                     if request.user.id != instance.user_id:
            ##                         return Response({'error': 'You are not authorized to perform this operation.'},
            ##                                         status=status.HTTP_401_UNAUTHORIZED)'''
            ##
            ##
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)


class PropertyAssetDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = PropertyAsset.objects.all()
    serializer_class = PropertyAssetSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TransportListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        brand = request.data['brand']
        name = request.data['name']

        mark, model = set_mark_model(brand, name)
        serializer.validated_data['mark'] = mark
        serializer.validated_data['model'] = model
        average_market, min_market, max_market = get_average(mark, model)
        serializer.validated_data['average_market_price'] = average_market
        serializer.validated_data['min_market_price'] = min_market
        serializer.validated_data['max_market_price'] = max_market


        # Check if an object with the same name already exists
        # if Transport.objects.filter(name=name).exists():
        #     return Response({'message': 'Object with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Property object
        self.perform_create(serializer)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)

        if serializer.instance.loan:
            # Create the Loans object
            loan = Loans(
                user_id=serializer.instance.user_id,
                name=serializer.instance.name,
                remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
                sum=serializer.instance.bought_price,
                loan_term=serializer.instance.loan_term,
                percentage=serializer.instance.percentage,
                month_payment=serializer.instance.month_payment,
                maintenance_cost=serializer.instance.month_expense
            )
            loan.save()
            serializer.instance.loan_link = loan
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
        income_instances = []
        expenses_instances = []

        if 'income' in request.data:
            income_data = request.data.pop('income')
            for income in income_data:
                income_serializer = IncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=1, property=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, property=instance)
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
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BusinessListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # name = request.data.get('name')
        # if Business.objects.filter(name=name).exists():
        #     return Response({'message': 'Object with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the Property object
        self.perform_create(serializer)

        # Check if the Property object has a non-empty loan field
        if serializer.instance.loan:
            # Create the Loans object
            loan = Loans(
                user_id=serializer.instance.user_id,
                name=serializer.instance.name,
                #remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
                sum=serializer.instance.bought_price,
                loan_term=serializer.instance.loan_term,
                percentage=serializer.instance.percentage,
                month_payment=serializer.instance.month_payment,
                maintenance_cost=serializer.instance.month_expense
            )
            loan.save()
            serializer.instance.loan_link = loan
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class BusinessUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    lookup_field = 'id'

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
                income_serializer = IncomeSerializer(data=income)
                income_serializer.is_valid(raise_exception=True)
                income_instance = income_serializer.save(user_id=1, property=instance)
                income_instances.append(income_instance)

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = ExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, property=instance)
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


class BusinessDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BusinessAssetListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = BusinessAsset.objects.all()
    serializer_class = BusinessAssetSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'business_id'

    def get_queryset(self):
        business_id = self.kwargs['business_id']
        queryset = BusinessAsset.objects.filter(business_id=business_id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BusinessAssetCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = BusinessAsset.objects.all()
    serializer_class = BusinessAssetSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            # loop through the list of dictionaries and create each object
            for obj_data in data:
                name = obj_data.get('name')
                if BusinessAsset.objects.filter(name=name).exists():
                    return Response({'message': f'Object with name {name} already exists.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            response_data = self.create(request, *args, **kwargs).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # create a single object
            name = data.get('name')
            if BusinessAsset.objects.filter(name=name).exists():
                return Response({'message': 'Object with this name already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)

            return self.create(request, *args, **kwargs)


class BusinessAssetUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = BusinessAsset.objects.all()
    serializer_class = BusinessAssetSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            obj_list = list()

            # If the request data is a list, loop through the objects and update them one by one
            for obj in request.data:
                self.queryset = BusinessAsset.objects.filter(id=obj['id'])
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=obj, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                obj_list.append(serializer.data)
            return Response(obj_list)

            # If the request data is not a list, assume it is a single object and update it
        instance = self.get_object()

        '''# Check if the user has the right to perform the update operation
        if request.user.id != instance.user_id:
            return Response({'error': 'You are not authorized to perform this operation.'},
                            status=status.HTTP_401_UNAUTHORIZED)'''

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BusinessAssetDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = BusinessAsset.objects.all()
    serializer_class = BusinessAssetSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StocksListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Stocks.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Stocks.objects.filter(name=name).exists():
            return Response({'message': 'Object with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)


class StocksUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Stocks.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        '''# Check if the user has the right to perform the update operation
        if request.user.id != instance.user_id:
            return Response({'error': 'You are not authorized to perform this operation.'},
                            status=status.HTTP_401_UNAUTHORIZED)'''

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class StocksDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Stocks.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BondsListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BondsUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        '''# Check if the user has the right to perform the update operation
        if request.user.id != instance.user_id:
            return Response({'error': 'You are not authorized to perform this operation.'},
                            status=status.HTTP_401_UNAUTHORIZED)'''

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BondsDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = [permissions.AllowAny]

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    def destroy_queryset(self, queryset):
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy_queryset(self.get_queryset())


class IncomeListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Income object
class IncomeDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ActiveList(generics.ListAPIView):
    serializer_class = ActivesSerializer
    permission_classes = [permissions.AllowAny]

    # permission_classes = [permissions.IsAuthenticated]
    def calculate_totals(self, user_id):
        # Calculate the total income from Income objects related to the user
        income_queryset = Income.objects.filter(user_id=user_id)
        total_income = income_queryset.aggregate(total_income=Sum('funds'))['total_income'] or 0

        # Calculate the total expenses from Expenses objects related to the user
        expenses_queryset = Expenses.objects.filter(user_id=user_id)
        total_expenses = expenses_queryset.aggregate(total_expenses=Sum('funds'))['total_expenses'] or 0

        return total_income, total_expenses

    def get(self, request, *args, **kwargs):
        user_id = 1
        actives, created = Actives.objects.get_or_create(user_id=user_id)

        # Retrieve properties, businesses, and transports related to the user
        properties = Property.objects.filter(user_id=user_id)
        businesses = Business.objects.filter(user_id=user_id)
        transports = Transport.objects.filter(user_id=user_id)

        # Calculate the total income and expenses from Income and Expenses objects related to the user
        total_income, total_expenses = self.calculate_totals(user_id)

        # Update the Actives object with the calculated totals
        actives.total_income = total_income
        actives.total_expenses = total_expenses

        actives.properties.set(properties)
        actives.businesses.set(businesses)
        actives.transports.set(transports)
        actives.save()

        # Return the serialized Actives object
        serializer = self.get_serializer(actives)
        return Response(serializer.data, status=status.HTTP_200_OK)

