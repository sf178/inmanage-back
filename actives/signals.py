from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .serializers import *
from passives.models import Loans, MainLoans
# from glob_parse.tasks import parse_avito_task
from balance import models as bal
from django.db import transaction
from balance.models import Card, Income, Expenses
from inventory.models import Inventory, InventoryAsset


@receiver(post_delete, sender=Property)
@receiver(post_delete, sender=Transport)
@receiver(post_delete, sender=Business)
def delete_linked_loan(sender, instance, **kwargs):
    # Проверяем, есть ли у экземпляра свойство 'loan' и удаляем связанный объект Loan, если он существует
    loan_attr = getattr(instance, 'loan', None)
    if loan_attr and isinstance(loan_attr, Loans):
        loan_attr.delete()


@receiver(post_save, sender=Jewelry)
def update_main_jewelries(sender, instance, created, **kwargs):
    main_jewelries = MainJewelry.objects.get(user=instance.user)
    # main_loans = MainLoans.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)  # получаем объект actives для этого пользователя

    if created:
        main_jewelries.jewelries.add(instance)
        main_jewelries.total_funds += instance.purchase_cost
        # if instance.loan:
        #     main_loans.total_funds -= instance.loan_link.sum
        #     main_loans.save(update_fields=['total_funds'])
        main_jewelries.save(update_fields=['total_funds'])
        actives.total_funds += instance.purchase_cost
        actives.save()


@receiver(post_delete, sender=Jewelry)
def delete_jewelries(sender, instance, **kwargs):
    main_jewelries = MainJewelry.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_jewelries.jewelries.remove(instance)

    main_jewelries.total_funds -= instance.purchase_cost

    main_jewelries.save(update_fields=['total_funds'])

    actives.total_funds -= instance.purchase_cost
    actives.save()


@receiver(post_save, sender=Securities)
def update_main_jewelries(sender, instance, created, **kwargs):
    main_securities = MainSecurities.objects.get(user=instance.user)
    # main_loans = MainLoans.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)  # получаем объект actives для этого пользователя

    if created:
        main_securities.securities.add(instance)
        main_securities.total_funds += instance.market_price
        # if instance.loan:
        #     main_loans.total_funds -= instance.loan_link.sum
        #     main_loans.save(update_fields=['total_funds'])
        main_securities.save(update_fields=['total_funds'])
        actives.total_funds += instance.market_price
        actives.save()


@receiver(post_delete, sender=Securities)
def delete_securities(sender, instance, **kwargs):
    main_securities = MainSecurities.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_securities.securities.remove(instance)

    main_securities.total_funds -= instance.market_price

    main_securities.save(update_fields=['total_funds'])

    actives.total_funds -= instance.market_price
    actives.save()


@receiver(post_save, sender=ActivesIncome)
def create_income_from_actives(sender, instance, created, **kwargs):
    if created:
        content_object = None
        card = Card.objects.get(id=instance.writeoff_account.id, user=instance.user)
        if instance.property:
            content_object = instance.property
        elif instance.transport:
            content_object = instance.transport
        elif instance.business:
            content_object = instance.business

        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            income_instance = Income.objects.create(
                user=instance.user,
                writeoff_account=instance.writeoff_account,
                funds=instance.funds,
                comment=instance.comment,
                content_type=content_type,
                object_id=content_object.id
            )
            card.income.add(income_instance)
            instance.child = income_instance
            instance.save(update_fields=['child'])


@receiver(post_save, sender=ActivesExpenses)
def create_expenses_from_actives(sender, instance, created, **kwargs):
    if created:
        card = Card.objects.get(id=instance.writeoff_account.id, user=instance.user)
        content_object = None
        if instance.property:
            content_object = instance.property
        elif instance.transport:
            content_object = instance.transport
        elif instance.business:
            content_object = instance.business

        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            expenses_instance = Expenses.objects.create(
                user=instance.user,
                writeoff_account=instance.writeoff_account,
                title=instance.title,
                description=instance.description,
                funds=instance.funds,
                content_type=content_type,
                object_id=content_object.id
            )
            card.expenses.add(expenses_instance)
            instance.child = expenses_instance
            instance.save(update_fields=['child'])


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


@receiver(post_delete, sender=Property)
def delete_property(sender, instance, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_properties.properties.remove(instance)

    main_properties.total_funds -= instance.actual_price
    main_properties.total_income -= instance.total_income
    main_properties.total_expenses -= instance.total_expense

    main_properties.save(update_fields=['total_funds', 'total_income', 'total_expenses'])

    actives.total_funds -= instance.actual_price
    actives.save()


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


@receiver(post_delete, sender=Business)
def delete_business(sender, instance, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_businesses.businesses.remove(instance)

    main_businesses.total_funds -= instance.equipment.total_actives_cost
    main_businesses.total_income -= instance.total_income
    main_businesses.total_expenses -= instance.total_expense
    main_businesses.save(update_fields=['total_funds', 'total_income', 'total_expenses'])

    actives.total_funds -= instance.revenue
    actives.save()

    if instance.card:
            instance.card.delete()


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


@receiver(post_delete, sender=Transport)
def delete_transport(sender, instance, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_transport.transport.remove(instance)
    main_transport.total_funds -= instance.bought_price
    main_transport.total_income -= instance.total_income
    main_transport.total_expenses -= instance.total_expense
    main_transport.save(update_fields=['total_funds', 'total_income', 'total_expenses'])

    actives.total_funds -= instance.bought_price
    actives.save()


@receiver(post_save, sender=Property)
def update_main_properties(sender, instance, created, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    main_loans = MainLoans.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)  # получаем объект actives для этого пользователя

    if created:
        main_properties.properties.add(instance)
        main_properties.total_funds += instance.actual_price
        if instance.loan:
            main_loans.total_funds -= instance.loan_link.sum
            main_loans.save(update_fields=['total_funds'])
        main_properties.save(update_fields=['total_funds'])
        actives.total_funds += instance.actual_price
        actives.save()


@transaction.atomic
def update_property_totals(sender, instance, created, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)  # получаем объект actives для этого пользователя

    # Эта проверка позволит избежать рекурсивного вызова функции обновления,
    # когда сама функция вызывает метод save() объекта Property.
    if hasattr(instance, '_updating_totals'):
        return

    instance._updating_totals = True

    old_income = instance.total_income or 0
    old_expense = instance.total_expense or 0

    # Проверяем, была ли изменена связь income или expenses.
    if sender == Property.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        change_in_income = instance.total_income - old_income
        main_properties.total_income += change_in_income
        actives.total_income += change_in_income
    elif sender == Property.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        change_in_expense = instance.total_expense - old_expense
        main_properties.total_expenses += change_in_expense
        actives.total_expenses += change_in_expense

    # сохраняем изменения
    instance.save(update_fields=['total_income', 'total_expense'])
    main_properties.save(update_fields=['total_income', 'total_expenses'])
    actives.save()

    del instance._updating_totals


@receiver(m2m_changed, sender=Property.income.through)
@receiver(m2m_changed, sender=Property.expenses.through)
def update_property_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_property_totals(sender=sender, instance=instance, created=False)


@receiver(post_save, sender=Transport)
def update_main_transport(sender, instance, created, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    main_loans = MainLoans.objects.get(user=instance.user)

    actives = Actives.objects.get(user=instance.user)
    if created:
        main_transport.transport.add(instance)
        main_transport.total_funds += instance.bought_price
        if instance.loan:
            main_loans.total_funds -= instance.loan_link.sum
            main_loans.save(update_fields=['total_funds'])
        main_transport.save(update_fields=['total_funds'])
        actives.total_funds += instance.bought_price
        actives.save()


@transaction.atomic
def update_transport_totals(sender, instance, created, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)

    # if created:
    #     main_transport.transport.add(instance)

    if hasattr(instance, '_updating_totals'):
        return

    instance._updating_totals = True

    old_income = instance.total_income or 0
    old_expense = instance.total_expense or 0

    # Проверяем, была ли изменена связь income или expenses.
    if sender == Transport.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        change_in_income = instance.total_income - old_income
        main_transport.total_income += change_in_income
        actives.total_income += change_in_income
    elif sender == Transport.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        change_in_expense = instance.total_expense - old_expense
        main_transport.total_expenses += change_in_expense
        actives.total_expenses += change_in_expense

    # сохраняем изменения
    instance.save(update_fields=['total_income', 'total_expense'])
    main_transport.save(update_fields=['total_income', 'total_expenses'])
    actives.save()

    del instance._updating_totals


@receiver(m2m_changed, sender=Transport.income.through)
@receiver(m2m_changed, sender=Transport.expenses.through)
def update_transport_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_transport_totals(sender=sender, instance=instance, created=False)


# @receiver(post_save, sender=Business)
@receiver(post_save, sender=Business)
def update_main_businesses(sender, instance, created, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    main_loans = MainLoans.objects.get(user=instance.user)

    actives = Actives.objects.get(user=instance.user)
    if created:
        main_businesses.businesses.add(instance)
        main_businesses.total_funds += instance.total_worth
        if instance.loan:
            main_loans.total_funds -= instance.loan_link.sum
            main_loans.save(update_fields=['total_funds'])
        main_businesses.save(update_fields=['total_funds'])
        actives.total_funds += instance.total_worth
        actives.save()


def update_business_totals(sender, instance, created, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)

    # if created:
    #     main_businesses.businesses.add(instance)

    if hasattr(instance, '_updating_totals'):
        return

    instance._updating_totals = True

    old_income = instance.total_income or 0
    old_expense = instance.total_expense or 0
    old_worth = instance.total_worth or 0
    # Проверяем, была ли изменена связь income или expenses.
    if sender == Business.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        change_in_income = instance.total_income - old_income
        main_businesses.total_income += change_in_income
        actives.total_income += change_in_income
    elif sender == Business.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        change_in_expense = instance.total_expense - old_expense
        main_businesses.total_expenses += change_in_expense
        actives.total_expenses += change_in_expense
    elif sender == Business.equipment.assets:
        instance.total_worth = instance.equipment.total_actives_cost
        # change_in_worth = instance.total_worth - old_worth
        # main_businesses.total_funds += change_in_worth

    # сохраняем изменения
    instance.save(update_fields=['total_income', 'total_expense', 'total_worth'])
    main_businesses.save(update_fields=['total_income', 'total_expenses'])
    actives.save()

    del instance._updating_totals


@receiver(m2m_changed, sender=Business.income.through)
@receiver(m2m_changed, sender=Business.expenses.through)
def update_business_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_business_totals(sender=sender, instance=instance, created=False)


@receiver(pre_save, sender=InventoryAsset)
@receiver(pre_delete, sender=InventoryAsset)
def inventory_asset_changed(sender, instance, **kwargs):
    # Проверяем, связан ли InventoryAsset с Inventory, который в свою очередь связан с Business
    if hasattr(instance, 'inventory') and instance.inventory:
        inventory = instance.inventory
        if inventory.content_type and inventory.content_type.model == 'business':
            business_instance = inventory.content_type.get_object_for_this_type(id=inventory.object_id)
            update_business_totals(sender=Business.equipment.assets, instance=business_instance)

@receiver(post_save, sender=Property)
def property_post_save(sender, instance, created, **kwargs):
    if created:
        src = 'actives'
        # parse_avito_task.delay(src=src, property_id=instance.id, city=instance.city, square=instance.square)

        # return HttpResponseRedirect(reverse('parser_view', args=[instance.id, instance.city, instance.square]))


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
