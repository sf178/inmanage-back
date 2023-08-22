from rest_framework import generics, mixins
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.response import Response


class InventoryListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class InventoryDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class InventoryUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        expenses_instances = []

        # Проверяем, есть ли 'assets' в данных запроса
        if 'assets' in request.data:
            assets_data = request.data.pop('assets')
            for asset_data in assets_data:
                asset_id = asset_data.get('id', None)
                delete_flag = asset_data.get('delete', False)

                if delete_flag and asset_id:
                    # Удаляем объект по ID
                    InventoryAsset.objects.filter(id=asset_id).delete()
                elif asset_id is None:
                    # Создаем новый объект
                    asset_serializer = InventoryAssetSerializer(data=asset_data)
                    asset_serializer.is_valid(raise_exception=True)
                    asset_instance = asset_serializer.save(user=instance.user)
                    instance.assets.add(asset_instance)
                elif asset_id:
                    # Обновляем существующий объект
                    asset_instance = InventoryAsset.objects.get(id=asset_id)
                    asset_serializer = InventoryAssetSerializer(asset_instance, data=asset_data, partial=True)
                    asset_serializer.is_valid(raise_exception=True)
                    asset_serializer.save()

        if 'expenses' in request.data:
            expenses_data = request.data.pop('expenses')
            for expense in expenses_data:
                expenses_serializer = InventoryExpensesSerializer(data=expense)
                expenses_serializer.is_valid(raise_exception=True)
                expenses_instance = expenses_serializer.save(user_id=1, inventory=instance)
                expenses_instances.append(expenses_instance)

                asset = InventoryAsset.objects.create(user=instance.user, text=expenses_instance.title, price=expenses_instance.funds)
                instance.assets.add(asset)

        # Обновляем основной объект Inventory
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if expenses_instances:
            instance.expenses.add(*[expense.id for expense in expenses_instances])

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        inventory = self.get_object()
        inventory.launch_status = False
        inventory.save()
        return Response(self.get_serializer(inventory).data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class InventoryAssetUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = InventoryAsset.objects.all()
    serializer_class = InventoryAssetSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class InventoryAssetDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = InventoryAsset.objects.all()
    serializer_class = InventoryAssetSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
