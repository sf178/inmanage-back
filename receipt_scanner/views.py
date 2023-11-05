from _decimal import Decimal
from datetime import datetime, timezone
import os
import environ

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Receipt, ReceiptItem
from .serializers import ReceiptSerializer, ReceiptItemSerializer

env = environ.Env()

class ReceiptAPI(APIView):

    def post(self, request, *args, **kwargs):
        url = 'https://proverkacheka.com/api/v1/check/get'

        request_data = request.data
        fn = request_data.get('fn')
        fd = request_data.get('fd')
        fp = request_data.get('fp')
        n = request_data.get('n')
        s = request_data.get('s')
        t = request_data.get('t')
        date_time_str = datetime.strptime(t, "%d.%m.%Y %H:%M")
        data = {
            'fn': fn,
            'fd': fd,
            'fp': fp,
            'n': n,
            's': s.replace('.', ''),  # Удаление точки из суммы
            't': date_time_str,  # Преобразование в нужный формат
            'token': env('receipt_tkn')  # Предполагая, что у вас есть токен
        }
        response = requests.post(url, data=data)
        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "Failed to decode JSON response"}, status=status.HTTP_400_BAD_REQUEST)

        # Извлечение данных из ответа
        receipt_info = response_data.get('data', {}).get('json', {})
        items = receipt_info.get('items', [])

        # Создание объекта Receipt
        receipt_info = response_data['data']['json']

        # Создание объекта Receipt
        receipt = Receipt.objects.create(
            user=receipt_info['user'],
            user_inn=receipt_info['userInn'].strip(),
            date_time=datetime.strptime(receipt_info['dateTime'], "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc),
            total_sum=Decimal(receipt_info['totalSum']) / 100,
            credit_sum=Decimal(receipt_info['creditSum']) / 100,
            cash_total_sum=Decimal(receipt_info['cashTotalSum']) / 100,
            ecash_total_sum=Decimal(receipt_info['ecashTotalSum']) / 100,
            retail_place=receipt_info['retailPlace'],
            retail_place_address=receipt_info['retailPlaceAddress'],
            shift_number=receipt_info['shiftNumber'],
            operation_type=receipt_info['operationType'],
            request_number=receipt_info['requestNumber'],
            fiscal_drive_number=receipt_info['fiscalDriveNumber'],
            fiscal_sign=receipt_info['fiscalSign'],
            fiscal_document_number=receipt_info['fiscalDocumentNumber'],
            fiscal_document_format_version=receipt_info['fiscalDocumentFormatVer'],
            kkt_registration_id=receipt_info['kktRegId'].strip(),
            applied_taxation_type=receipt_info['appliedTaxationType'],
            nds_18=Decimal(receipt_info['nds18']) / 100,
        )

        # Создание объектов ReceiptItem
        for item_info in receipt_info['items']:
            ReceiptItem.objects.create(
                receipt=receipt,
                name=item_info['name'],
                price=Decimal(item_info['price']) / 100,
                quantity=Decimal(item_info['quantity']),
                sum=Decimal(item_info['sum']) / 100,
                nds=item_info['nds'],
                payment_type=item_info['paymentType'],
                product_type=item_info['productType'],
            )
        # Возвращение созданного объекта Receipt в формате JSON
        receipt_serializer = ReceiptSerializer(receipt)
        return Response(receipt_serializer.data, status=status.HTTP_201_CREATED)
