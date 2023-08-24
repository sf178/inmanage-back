from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import *
from actives import models as act
from passives import models as pas
from .views import BalanceListView
from django.db import transaction

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

# @receiver(post_save, sender=Card)
def update_card_totals(sender, instance, **kwargs):
    balance = Balance.objects.get(user=instance.user)
    if hasattr(instance, '_updating_totals'):
        # Возвращаемся назад, если объект уже обновляется в этом сигнале
        return

    instance._updating_totals = True
    old_income = instance.total_income or 0
    old_expense = instance.total_expense or 0
    instance.save(update_fields=['total_income', 'total_expense'])
    if sender == Card.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        # change_in_income = instance.total_income - old_income
        # balance.total_income += change_in_income
    elif sender == Card.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        # change_in_expense = instance.total_expense - old_expense
        # balance.total_expenses += change_in_expense
    instance.save(update_fields=['total_income', 'total_expense'])

    del instance._updating_totals


@receiver(m2m_changed, sender=Card.income.through)
@receiver(m2m_changed, sender=Card.expenses.through)
def update_property_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_card_totals(sender=sender, instance=instance, created=False)


def decrease_remainder(card, instance):
    card.remainder = card.remainder - instance.funds
    card.save(update_fields=['remainder'])


def increase_remainder(card, instance):
    card.remainder = card.remainder + instance.funds
    card.save(update_fields=['remainder'])


@receiver(post_save, sender=Expenses)
@receiver(post_save, sender=Income)
def decrease_card_remainder(sender, instance, created, **kwargs):
    card = instance.card
    if card:
        if sender == Expenses:
            decrease_remainder(card, instance)
        if sender == Income:
            increase_remainder(card, instance)


@receiver(post_delete, sender=Expenses)
@receiver(post_delete, sender=Income)
def increase_card_remainder(sender, instance, **kwargs):
    card = instance.card
    if card:
        if sender == Expenses:
            increase_remainder(card, instance)
        if sender == Income:
            decrease_remainder(card, instance)
