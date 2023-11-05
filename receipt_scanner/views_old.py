from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import asyncio
from asgiref.sync import async_to_sync

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .models import Receipt, ReceiptItem  # Импорт ваших моделей
from .scanner import main
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Receipt, ReceiptItem
from .serializers import ReceiptSerializer, ReceiptItemSerializer
from django.shortcuts import get_object_or_404
from test_backend.custom_methods import IsAuthenticatedCustom


class ReceiptView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    async def get_receipt_info(self, receipt_info):
        # Замените вызов check_receipt на main из scanner.py
        return await main(receipt_info)

    def post(self, request, *args, **kwargs):
        receipt_info = request.data  # Изменено для DRF

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Запуск вашего скрипта с данными из запроса
            response_data = async_to_sync(self.get_receipt_info)(receipt_info)
        finally:
            loop.close()
        # Создание и сохранение экземпляра Receipt
        receipt = Receipt(
            date_time=response_data['date_time'],
            total_amount=response_data['total_amount'],
            user=response_data['user'],
            retail_place_address=response_data['retail_place_address'],
            shift_number=response_data['shift_number'],
            taxation_type=response_data['taxation_type'],
            electronic_amount=response_data['electronic_amount'],
            fiscal_sign=response_data['fiscal_sign'],
            request_number=response_data['request_number'],
            fiscal_document_number=response_data['fiscal_document_number'],
            fiscal_document_format_version=response_data['fiscal_document_format_version'],
        )
        receipt.save()

        # Создание и сохранение экземпляров ReceiptItem
        for item_data in response_data['items']:
            item = ReceiptItem(
                receipt=receipt,
                item_number=item_data['item_number'],
                name=item_data['name'],
                price=item_data['price'],
                quantity=item_data['quantity']
            )
            item.save()

        return Response(response_data, status=status.HTTP_200_OK)  # Изменено для DRF


class ListUserReceiptsView(generics.ListAPIView):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        user = self.request.user  # Получение текущего пользователя
        return Receipt.objects.filter(user=user)  # Фильтрация чеков по пользователю


class DeleteReceiptView(generics.DestroyAPIView):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        receipt_id = self.kwargs['pk']  # Получение ID чека из URL
        return get_object_or_404(Receipt, id=receipt_id)  # Получение объекта чека или возвращение 404, если он не найден

    def delete(self, request, *args, **kwargs):
        receipt = self.get_object()
        receipt.delete()
        return Response(status=204)  # Возвращение статуса 204 (No Content) при успешном удалении