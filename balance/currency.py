import json
import requests
from django.http import JsonResponse
from django_background_tasks import background
from balance.models import Currency


def get_exchange_rates(api_key, base='USD'):
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("Ошибка при получении данных:", response.status_code)
        return None


def convert_to_rub(rates, rub_rate):
    converted_rates = {}
    for currency, rate in rates.items():
        # Пересчет курса валюты к RUB
        converted_rates[currency] = rub_rate / rate
    return converted_rates


def get_rates_in_rub(api_key, currencies):
    rates = get_exchange_rates(api_key)
    if rates:
        rub_exchange_rate = rates['rates']['RUB']
        rates_in_rub = convert_to_rub(rates['rates'], rub_exchange_rate)
        return {currency: rates_in_rub[currency] for currency in currencies}


@background(schedule=60*60*24)
def currency_rates_task():
    api_key = 'db8d9f75688041cf831131e1b35655e3'  # Установите ваш API ключ
    currencies = ['EUR', 'GBP', 'JPY', 'CNY', 'USD']  # Выбранные валюты

    rates_in_rub = get_rates_in_rub(api_key, currencies)
    if rates_in_rub:
        for currency, rate in rates_in_rub.items():
            Currency.objects.update_or_create(name=currency, defaults={'price': rate})

        # return JsonResponse(rates_in_rub)
    else:
        return JsonResponse({'error': 'Не удалось получить данные о курсах валют'}, status=500)


