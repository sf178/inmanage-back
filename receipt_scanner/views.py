import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Receipt, ReceiptItem
from .serializers import ReceiptSerializer, ReceiptItemSerializer


class ReceiptAPI(APIView):

    def post(self, request, *args, **kwargs):
        url = 'https://proverkacheka.com/api/v1/check/get'

        data = request.data

        response = requests.post(url, data=data)
        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "Failed to decode JSON response"}, status=status.HTTP_400_BAD_REQUEST)

        # Извлечение данных из ответа
        receipt_info = response_data.get('data', {}).get('json', {})
        items = receipt_info.get('items', [])

        # Создание объекта Receipt
        receipt_data = {
            'date_time': receipt_info.get('dateTime'),
            'total_amount': float(receipt_info.get('totalSum', 0)) / 100,
            'user': receipt_info.get('user'),
            'retail_place_address': receipt_info.get('retailPlaceAddress'),
            'shift_number': receipt_info.get('shiftNumber'),
            'taxation_type': receipt_info.get('appliedTaxationType'),
            'electronic_amount': float(receipt_info.get('ecashTotalSum', 0)) / 100,
            'fiscal_sign': receipt_info.get('fiscalSign'),
            'request_number': receipt_info.get('requestNumber'),
            'fiscal_document_number': receipt_info.get('fiscalDocumentNumber'),
            'fiscal_document_format_version': receipt_info.get('fiscalDocumentFormatVer'),
        }
        receipt_serializer = ReceiptSerializer(data=receipt_data)
        if receipt_serializer.is_valid():
            receipt = receipt_serializer.save()
        else:
            return Response(receipt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Создание объектов ReceiptItem
        for i, item in enumerate(items):
            item_data = {
                'receipt': receipt.id,
                'item_number': i + 1,
                'name': item.get('name'),
                'price': float(item.get('price', 0)) / 100,
                'quantity': item.get('quantity')
            }
            item_serializer = ReceiptItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Возвращение созданного объекта Receipt в формате JSON
        receipt_serializer = ReceiptSerializer(receipt)
        return Response(receipt_serializer.data, status=status.HTTP_201_CREATED)
