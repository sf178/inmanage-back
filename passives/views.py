from rest_framework import generics, permissions, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

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
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
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

        # Create the Property object
        self.perform_create(serializer)

        # Check if the Property object has a non-empty loan field
        if serializer.instance.loan:
            # Create the Loans object
            loan = Loans(
                user_id=serializer.instance.user_id,
                name=serializer.instance.name,
                # remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
                sum=serializer.instance.bought_price,
                loan_term=serializer.instance.loan_term,
                percentage=serializer.instance.percentage,
                month_payment=serializer.instance.month_payment,
                maintenance_cost=serializer.instance.month_expense
            )
            loan.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class PropertyUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PropertyDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Property.objects.filter(user_id='1')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        brand = request.data['brand']
        name = request.data['name']

        mark, model = set_mark_model(brand, name)

        # serializer.mark = mark
        # serializer.model = model

        serializer.validated_data['mark'] = brand
        serializer.validated_data['model'] = name
        average_market, min_market, max_market = get_average(mark, model)
        # serializer.average_market_price = average_market
        # serializer.min_market_price = min_market
        # serializer.max_market_price = max_market

        serializer.validated_data['average_market_price'] = average_market
        serializer.validated_data['min_market_price'] = min_market
        serializer.validated_data['max_market_price'] = max_market

        # Create the Property object
        self.perform_create(serializer)

        # Check if the Property object has a non-empty loan field
        if serializer.instance.loan:
            # Create the Loans object
            loan = Loans(
                user_id=serializer.instance.user_id,
                name=serializer.instance.name,
                # remainder=serializer.instance.actual_price - serializer.instance.initial_payment,
                sum=serializer.instance.bought_price,
                loan_term=serializer.instance.loan_term,
                percentage=serializer.instance.percentage,
                month_payment=serializer.instance.month_payment,
                maintenance_cost=serializer.instance.month_expense
            )
            loan.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class TransportUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TransportDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PassivesCreateView(generics.CreateAPIView):
    queryset = Passives.objects.all()
    serializer_class = PassivesSerializer

    def create(self, request, *args, **kwargs):
        # Calculate the total funds from Expenses objects
        total_funds = Expenses.objects.aggregate(total_funds=Sum('funds'))['total_funds']

        # Create the Passives object with the calculated total funds
        passives = Passives(total_funds=total_funds)
        passives.save()

        # Return the serialized Passives object
        serializer = self.get_serializer(passives)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# View mixin for listing all Expenses objects and creating new Expenses objects
class ExpensesListView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# View mixin for retrieving, updating, and deleting a specific Expenses object
class ExpensesDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)