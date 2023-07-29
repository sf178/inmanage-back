from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from actives.models import Actives
from passives.models import Passives
from .views import BalanceListView

@receiver(post_save, sender=Actives)
@receiver(post_save, sender=Passives)
@receiver(post_save, sender=Card)
def update_balance(sender, instance, **kwargs):
    user = instance.user
    balance = Balance.objects.get(user=user)  # or create a new one

    total_income, total_expenses, total = BalanceListView.calculate_totals(sender, user)

    balance.total_income = total_income
    balance.total_expenses = total_expenses
    balance.total = total
    balance.save()