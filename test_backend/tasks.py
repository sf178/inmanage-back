from balance.currency import *
from celery import shared_task


@shared_task
def update_currency_rates():
    currency_rates_view()
