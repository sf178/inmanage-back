from rest_framework import generics, permissions, mixins
from django.db.models import Sum, Q
from .models import Card, Balance, Expenses, Income
from rest_framework.response import Response
from .serializers import CardSerializer, BalanceSerializer


class CardListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CardDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BalanceListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.AllowAny]
    from rest_framework import generics
    from django.db.models import Sum, Q
    from .models import Balance, Income, Expenses
    from .serializers import BalanceSerializer

    class BalanceView(generics.RetrieveAPIView, generics.ListCreateAPIView):
        serializer_class = BalanceSerializer

        def get_object(self):
            # Retrieve the user ID from the request (Assuming you have a way to identify the user)
            user_id = self.request.user.id

            # Calculate total_expenses from all Expenses objects in the actives, passives, and balance apps
            total_expenses = Expenses.objects.filter(
                Q(card__user_id=user_id) |  # Related to the balance app
                Q(property__transport__user_id=user_id) |  # Related to the passives app
                Q(property__business__user_id=user_id)  # Related to the actives app
            ).aggregate(total_expenses=Sum('funds'))['total_expenses'] or 0

            # Calculate total_income from all Income objects in the actives, passives, and balance apps
            total_income = Income.objects.filter(
                Q(card__user_id=user_id) |  # Related to the balance app
                Q(property__transport__user_id=user_id) |  # Related to the passives app
                Q(property__business__user_id=user_id)  # Related to the actives app
            ).aggregate(total_income=Sum('funds'))['total_income'] or 0

            # Create or retrieve the Balance object for the user
            balance, _ = Balance.objects.get_or_create(user_id=user_id)

            # Update the Balance object with the calculated totals
            balance.total_expenses = total_expenses
            balance.total_income = total_income

            # Calculate the total field (if needed)
            balance.total = balance.total_income - balance.total_expenses

            # Save the updated Balance object
            balance.save()

            return balance

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate total expenses from all apps
        total_expenses = Expenses.objects.filter(Q(card__in=instance.card_list.all()) | Q(card__isnull=True)).aggregate(
            total_expenses=Sum('funds'))['total_expenses']
        if total_expenses is not None:
            instance.total_expenses = total_expenses

        # Calculate total income from all apps
        total_income = Income.objects.filter(Q(card__in=instance.card_list.all()) | Q(card__isnull=True)).aggregate(
            total_income=Sum('funds'))['total_income']
        if total_income is not None:
            instance.total_income = total_income

        # Calculate the remaining total if both total_expenses and total_income are present
        if instance.total_expenses is not None and instance.total_income is not None:
            instance.total = instance.total_income - instance.total_expenses

        # Save the updated instance
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # instance = Balance.objects.filter(user__id=request.data['user'])
        # #for object in instance:
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)
        #return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BalanceUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BalanceDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
