from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from actives import models as act
from passives import models as pas
from .views import BalanceListView

@receiver(post_save, sender=act.Actives)
@receiver(post_save, sender=pas.Passives)
@receiver(post_save, sender=Card)
def update_balance(sender, instance, **kwargs):
    user = instance.user
    balance = Balance.objects.get(user=user)  # or create a new one

    total_income, total_expenses, total, card_funds, card_income, card_expenses = BalanceListView.calculate_totals(user)

    balance.total_income = total_income
    balance.total_expenses = total_expenses
    balance.total = total
    balance.card_funds = card_funds
    balance.card_income = card_income
    balance.card_expenses = card_expenses
    balance.save()


@receiver(post_save, sender=act.ActivesExpenses)
@receiver(post_save, sender=pas.Expenses)
def update_card_expenses(sender, instance, created, **kwargs):
    """
    При создании объекта ActivesExpenses обновляет поле expenses у соответствующего объекта Card.
    """
    if created:  # Проверяем, что объект был создан, а не обновлен
        card = instance.writeoff_account
        if card:
            expenses = Expenses.objects.create(
                user=instance.user,
                card=card,
                title=instance.title,
                description=instance.description,
                funds=instance.funds,
            )
            category_value = instance.category
            if category_value:  # Проверка, что значение не None и не пустое
                if category_value not in expenses.category:
                    expenses.category.append(category_value)
                    expenses.save(update_fields=['category'])

            # Связываем объект Expenses с объектом Card
            card.expenses.add(expenses)
            card.save()


@receiver(post_save, sender=Expenses)
def decrease_card_remainder(sender, instance, created, **kwargs):
    card = instance.card
    if card:
        card.remainder = card.remainder - instance.funds
        card.save(update_fields=['remainder'])


@receiver(post_delete, sender=Expenses)
def increase_card_remainder(sender, instance, created, **kwargs):
    card = instance.card
    if card:
        card.remainder = card.remainder + instance.funds
        card.save(update_fields=['remainder'])
