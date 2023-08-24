from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import *
from .serializers import *
from passives.models import Loans
from balance import models as bal


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

@receiver(post_save, sender=Business)
def create_loan_business(sender, instance, created, **kwargs):
    if created and instance.loan:
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.name,
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
            name=instance.mark + instance.model,
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


# @receiver(post_save, sender=Property)
def update_property_totals(sender, instance, created, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)  # получаем объект actives для этого пользователя

    if created:
        main_properties.properties.add(instance)

    if hasattr(instance, '_updating_totals'):
        return

    instance._updating_totals = True
    # instance = Property.objects.get(id=instance.id)
    instance.total_income = sum(income.funds for income in instance.income.all())
    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_income', 'total_expense'])

    main_properties.total_income += instance.total_income
    main_properties.total_expenses += instance.total_expense
    main_properties.total_funds += instance.actual_price
    main_properties.save(update_fields=['total_income', 'total_expenses', 'total_funds'])

    actives.total_income += instance.total_income
    actives.total_expenses += instance.total_expense
    actives.total_funds += instance.actual_price
    actives.save()

    del instance._updating_totals

@receiver(m2m_changed, sender=Property.income.through)
@receiver(m2m_changed, sender=Property.expenses.through)
def update_property_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_property_totals(sender=Property, instance=instance, created=False)


# @receiver(post_save, sender=Transport)
def update_transport_totals(sender, instance, created, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)

    if created:
        main_transport.transport.add(instance)

    if hasattr(instance, '_updating_totals'):
        return
    instance._updating_totals = True
    instance.total_income = sum(income.funds for income in instance.income.all())
    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_income', 'total_expense'])

    main_transport.total_income += instance.total_income
    main_transport.total_expenses += instance.total_expense
    main_transport.total_funds += instance.bought_price
    main_transport.save(update_fields=['total_income', 'total_expenses', 'total_funds'])

    actives.total_income += instance.total_income
    actives.total_expenses += instance.total_expense
    actives.total_funds += instance.bought_price
    actives.save()

    del instance._updating_totals


@receiver(m2m_changed, sender=Transport.income.through)
@receiver(m2m_changed, sender=Transport.expenses.through)
def update_transport_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_transport_totals(sender=Transport, instance=instance, created=False)

# @receiver(post_save, sender=Business)
def update_business_totals(sender, instance, created, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)

    if created:
        main_businesses.businesses.add(instance)

    if hasattr(instance, '_updating_totals'):
        return

    instance._updating_totals = True
    instance.total_income = sum(income.funds for income in instance.income.all())
    instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
    instance.save(update_fields=['total_income', 'total_expense'])

    main_businesses.total_income += instance.total_income
    main_businesses.total_expenses += instance.total_expense
    main_businesses.total_funds += instance.revenue
    main_businesses.save(update_fields=['total_income', 'total_expenses', 'total_funds'])

    actives.total_income += instance.total_income
    actives.total_expenses += instance.total_expense
    actives.total_funds += instance.revenue
    actives.save()

    del instance._updating_totals

@receiver(m2m_changed, sender=Business.income.through)
@receiver(m2m_changed, sender=Business.expenses.through)
def update_business_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_business_totals(sender=Business, instance=instance, created=False)


# def update_main_totals(instance, related_field):
#     total_funds = 0.0
#     total_income = 0.0
#     total_expenses = 0.0
#     related_objects = getattr(instance, related_field).all()
#
#     for obj in related_objects:
#         total_funds += getattr(obj, 'actual_price', 0.0) or getattr(obj, 'revenue', 0.0) or getattr(obj, 'bought_price', 0.0)
#         total_income += getattr(obj, 'total_income', 0.0)
#         total_expenses += getattr(obj, 'total_expense', 0.0)
#
#     instance.total_funds = total_funds
#     instance.total_income = total_income
#     instance.total_expenses = total_expenses
#     instance.save(update_fields=['total_funds', 'total_income', 'total_expenses']) # update_fields=['total_funds', 'total_income', 'total_expenses']   -   в скобки



# @receiver(m2m_changed, sender=MainProperties.properties.through)
# def update_main_properties_totals(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         update_main_totals(instance, 'properties')


# @receiver(m2m_changed, sender=MainTransport.transport.through)
# def update_main_transport_totals(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         update_main_totals(instance, 'transport')
#
#
# @receiver(m2m_changed, sender=MainBusinesses.businesses.through)
# def update_main_businesses_totals(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         update_main_totals(instance, 'businesses')


# @receiver(post_save, sender=MainProperties)
# @receiver(post_save, sender=MainTransport)
# @receiver(post_save, sender=MainBusinesses)
# def update_actives_totals(sender, instance, created, **kwargs):
#     # Получение объекта Actives, связанного с объектом, который был сохранен
#     if not created:
#         actives = Actives.objects.get(user=instance.user)
#         total_funds = 0
#         total_income = 0
#         total_expenses = 0
#         if actives.properties:
#             total_funds += actives.properties.total_funds or 0
#             total_income += actives.properties.total_income or 0
#             total_expenses += actives.properties.total_expenses or 0
#         if actives.transports:
#             total_funds += actives.transports.total_funds or 0
#             total_income += actives.transports.total_income or 0
#             total_expenses += actives.transports.total_expenses or 0
#         if actives.businesses:
#             total_funds += actives.businesses.total_funds or 0
#             total_income += actives.businesses.total_income or 0
#             total_expenses += actives.businesses.total_expenses or 0
#
#         # Сохранение обновленного объекта Actives
#         actives.total_funds = total_funds
#         actives.total_income = total_income
#         actives.total_expenses = total_expenses
#         actives.save() # update_fields=['total_funds', 'total_income', 'total_expenses']
