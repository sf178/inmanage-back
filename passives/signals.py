from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import *
from .serializers import *


@receiver(post_save, sender=Property)
def create_loan_property(sender, instance, created, **kwargs):
    if created and instance.loan:
        initial_payment = instance.initial_payment or 0
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.name,
            remainder=instance.actual_price - initial_payment,
            sum=instance.bought_price,
            loan_term=instance.loan_term,
            percentage=instance.percentage,
            month_payment=instance.month_payment,
            maintenance_cost=instance.month_expense
        )
        loan.save()
        instance.loan_link = loan
        instance.save(update_fields=['loan_link'])


@receiver(post_save, sender=Transport)
def create_loan_transport(sender, instance, created, **kwargs):
    if created and instance.loan:
        initial_payment = instance.initial_payment or 0
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.name,
            remainder=instance.bought_price - initial_payment,
            sum=instance.bought_price,
            loan_term=instance.loan_term,
            percentage=instance.percentage,
            month_payment=instance.month_payment,
            maintenance_cost=instance.month_expense
        )
        loan.save()
        instance.loan_link = loan
        instance.save(update_fields=['loan_link'])

@receiver(post_save, sender=Property)
def update_property_totals(sender, instance, created, **kwargs):
    if created:
        main_properties = MainProperties.objects.get(user=instance.user)
        main_properties.properties.add(instance)
    if hasattr(instance, '_updating_totals'):
        # Возвращаемся назад, если объект уже обновляется в этом сигнале
        return
    instance._updating_totals = True

    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_expense'])
    del instance._updating_totals




@receiver(post_save, sender=Transport)
def update_transport_totals(sender, instance, created, **kwargs):
    if created:
        main_transport = MainTransport.objects.get(user=instance.user)
        main_transport.transport.add(instance)
    if hasattr(instance, '_updating_totals'):
        # Возвращаемся назад, если объект уже обновляется в этом сигнале
        return
    instance._updating_totals = True

    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_expense'])
    del instance._updating_totals



@receiver(post_save, sender=Loans)
def update_loans_totals(sender, instance, created, **kwargs):
    if created:
        main_loans = MainLoans.objects.get(user=instance.user)
        main_loans.loans.add(instance)
    if hasattr(instance, '_updating_totals'):
        # Возвращаемся назад, если объект уже обновляется в этом сигнале
        return
    instance._updating_totals = True

    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_expense'])
    del instance._updating_totals



def update_main_totals(instance, related_field):
    total_funds = 0.0
    total_expenses = 0.0
    related_objects = getattr(instance, related_field).all()

    for obj in related_objects:
        total_funds += getattr(obj, 'actual_price', 0.0) or getattr(obj, 'remainder', 0.0) or getattr(obj, 'bought_price', 0.0)
        total_expense = getattr(obj, 'total_expense', 0.0)
        total_expenses += total_expense if total_expense is not None else 0.0

    if hasattr(instance, 'total_funds'):
        instance.total_funds = total_funds
        instance.save(update_fields=['total_funds'])
    instance.total_expenses = total_expenses
    instance.save() # update_fields=['total_expenses']


@receiver(m2m_changed, sender=MainProperties.properties.through)
def update_main_properties_totals(sender, instance, action, **kwargs):
    if action == 'post_add':
        update_main_totals(instance, 'properties')


@receiver(m2m_changed, sender=MainTransport.transport.through)
def update_main_transport_totals(sender, instance, action, **kwargs):
    if action == 'post_add':
        update_main_totals(instance, 'transport')


@receiver(m2m_changed, sender=MainLoans.loans.through)
def update_main_loans_totals(sender, instance, action, **kwargs):
    if action == 'post_add':
        update_main_totals(instance, 'loans')


@receiver(post_save, sender=MainProperties)
@receiver(post_save, sender=MainTransport)
@receiver(post_save, sender=MainLoans)
def update_passives_totals(sender, instance, **kwargs):
    passives = Passives.objects.get(user=instance.user)
    total_funds = 0
    total_expenses = 0
    if passives.properties:
        total_funds += passives.properties.total_funds or 0
        total_expenses += passives.properties.total_expenses or 0
    if passives.transports:
        total_funds += passives.transports.total_funds or 0
        total_expenses += passives.transports.total_expenses or 0
    if passives.loans:
        total_funds += passives.loans.total_funds or 0
        total_expenses += passives.loans.total_expenses or 0

    # Получение объектов MainProperties, MainTransport и MainLoans для данного пользователя
    # total_funds = (passives.properties.total_funds or 0) + (passives.transports.total_funds or 0) + \
    #               (passives.loans.total_funds or 0)
    # total_expenses = (passives.properties.total_expenses or 0) + (passives.transports.total_expenses or 0) + \
    #                  (passives.loans.total_expenses or 0)
    # Суммирование полей total_funds и total_expenses из всех связанных объектов
    passives.total_funds = total_funds
    passives.total_expenses = total_expenses

    # Сохранение обновленного объекта Passives
    passives.save()



