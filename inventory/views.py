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


class InventoryUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем, есть ли 'assets' в данных запроса
        if 'assets' in request.data:
            assets_data = request.data.pop('assets')
            for asset_data in assets_data:
                # Создаем новый объект для каждого имущества в данных
                asset_serializer = InventoryAssetSerializer(data=asset_data)
                asset_serializer.is_valid(raise_exception=True)
                asset_instance = asset_serializer.save(user=instance.user)

                # Добавляем созданный объект имущества к инвентаризации
                instance.assets.add(asset_instance)

        # Обновляем основной объект Inventory
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class InventoryAssetDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = InventoryAsset.objects.all()
    serializer_class = InventoryAssetSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
