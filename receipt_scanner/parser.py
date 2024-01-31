# # import json
#
#
# # def format_response(response_body):
# #     response_json = json.loads(response_body)
# #
# #     receipt_info = response_json.get('receipt', {})
# #     items = receipt_info.get('items', [])
# #
# #     print("1. Общая информация о чеке:")
# #     print(f"   - Дата и время: {receipt_info.get('dateTime')}")
# #     print(f"   - Сумма: {receipt_info.get('totalSum') / 100} рублей")
# #     print(f"   - Пользователь: {receipt_info.get('user')}")
# #     print(f"   - Адрес розничного места: {receipt_info.get('retailPlace')}")
# #     print()
# #
# #     print("2. Элементы чека:")
# #     for i, item in enumerate(items, 1):
# #         print(
# #             f"   - Товар {i}: {item.get('name')}, Цена: {item.get('price') / 100} рублей, Количество: {item.get('quantity')}")
# #     print()
# #
# #     print("3. Дополнительная информация:")
# #     print(f"   - Номер смены: {receipt_info.get('shiftNumber')}")
# #     print(f"   - Тип налогообложения: {receipt_info.get('taxationType')}")
# #     print(f"   - Электронная сумма: {receipt_info.get('ecashTotalSum') / 100} рублей")
# #     print(f"   - Фискальный знак: {receipt_info.get('fiscalSign')}")
# #     print(f"   - Номер запроса: {receipt_info.get('requestNumber')}")
# #     print(f"   - Номер фискального документа: {receipt_info.get('fiscalDocumentNumber')}")
# #     print(f"   - Версия формата фискального документа: {receipt_info.get('fiscalDocumentFormatVer')}")
#
# import json
#
#
# def format_response(response_body):
#     response_json = json.loads(response_body)
#
#     receipt_info = response_json.get('receipt', {})
#     items = receipt_info.get('items', [])
#
#     formatted_response = {
#         "general_information": {
#             "date_time": receipt_info.get('dateTime'),
#             "total_amount": receipt_info.get('totalSum') / 100,
#             "user": receipt_info.get('user'),
#             "retail_place_address": receipt_info.get('retailPlace'),
#         },
#         "receipt_items": [
#             {
#                 "item_number": i + 1,
#                 "name": item.get('name'),
#                 "price": item.get('price') / 100,
#                 "quantity": item.get('quantity')
#             } for i, item in enumerate(items)
#         ],
#         "additional_information": {
#             "shift_number": receipt_info.get('shiftNumber'),
#             "taxation_type": receipt_info.get('taxationType'),
#             "electronic_amount": receipt_info.get('ecashTotalSum') / 100,
#             "fiscal_sign": receipt_info.get('fiscalSign'),
#             "request_number": receipt_info.get('requestNumber'),
#             "fiscal_document_number": receipt_info.get('fiscalDocumentNumber'),
#             "fiscal_document_format_version": receipt_info.get('fiscalDocumentFormatVer')
#         }
#     }
#
#     return json.dumps(formatted_response, ensure_ascii=False, indent=4)
#
#
