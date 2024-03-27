from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .serializers import *
from passives.models import Loans, MainLoans
from balance import models as bal
from django.db import transaction
from balance.models import Card, Income, Expenses
from inventory.models import Inventory, InventoryAsset


@receiver(post_delete, sender=Property)
@receiver(post_delete, sender=Transport)
@receiver(post_delete, sender=Business)
def delete_linked_loan(sender, instance, **kwargs):
    loan_attr = getattr(instance, 'loan', None)
    if loan_attr and isinstance(loan_attr, Loans):
        loan_attr.delete()


# Обновление сумм (Ювелирка, Бумаги, Вклады)
@transaction.atomic
def set_mainjewerlies(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.estimated_cost for prop in instance.jewelries.all())
    instance.save(update_fields=['total_funds'])
    del instance._count


@receiver(m2m_changed, sender=MainJewelry.jewelries.through)
def set_mainjewelries_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_mainjewerlies(sender=sender, instance=instance, created=False)


@receiver(post_save, sender=Jewelry)
def update_main_jewelries(sender, instance, created, **kwargs):
    main_jewelries = MainJewelry.objects.get(user=instance.user)
    if created:
        main_jewelries.jewelries.add(instance)


@receiver(post_delete, sender=Jewelry)
def delete_jewelries(sender, instance, **kwargs):
    main_jewelries = MainJewelry.objects.get(user=instance.user)
    main_jewelries.jewelries.remove(instance)


@receiver(post_save, sender=Securities)
def update_main_securities(sender, instance, created, **kwargs):
    if hasattr(instance, '_updating'):
        return
    try:
        instance._updating = True
        main_securities = MainSecurities.objects.get(user=instance.user)
        instance.sum = instance.count * instance.cost
        instance.save(update_fields=['sum'])
        if created:
            main_securities.securities.add(instance)
    finally:
        del instance._updating


@transaction.atomic
def set_mainsecurities(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.cost for prop in instance.securities.all())
    instance.save(update_fields=['total_funds'])
    del instance._count


@receiver(m2m_changed, sender=MainSecurities.securities.through)
def set_mainsecurities_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_mainsecurities(sender=sender, instance=instance, created=False)


@receiver(post_delete, sender=Securities)
def delete_securities(sender, instance, **kwargs):
    main_securities = MainSecurities.objects.get(user=instance.user)
    main_securities.securities.remove(instance)


@receiver(post_save, sender=ActivesDeposit)
def update_main_deposits(sender, instance, created, **kwargs):
    main_deposits = MainDeposits.objects.get(user=instance.user)
    if created:
        main_deposits.deposits.add(instance)


@receiver(post_delete, sender=ActivesDeposit)
def delete_deposits(sender, instance, **kwargs):
    main_deposits = MainDeposits.objects.get(user=instance.user)
    main_deposits.deposits.remove(instance)


@transaction.atomic
def set_maindeposits(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.sum for prop in instance.deposits.all())
    instance.save(update_fields=['total_funds'])
    del instance._count


@receiver(m2m_changed, sender=MainDeposits.deposits.through)
def set_maindeposits_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_maindeposits(sender=sender, instance=instance, created=False)


@transaction.atomic
def set_mainsecurities(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.sum for prop in instance.securities.all())
    instance.save(update_fields=['total_funds'])
    del instance._count


@receiver(m2m_changed, sender=MainSecurities.securities.through)
def set_mainsecurities_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_mainsecurities(sender=sender, instance=instance, created=False)


# Конец раздела

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
        content_type = ContentType.objects.get_for_model(instance)
        initial_payment = instance.initial_payment or 0
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.name,
            remainder=instance.actual_price - initial_payment,
            sum=instance.bought_price,
            loan_term=instance.loan_term,
            percentage=instance.percentage,
            month_payment=instance.month_payment,
            maintenance_cost=instance.month_expense,
            content_type=content_type,
            object_id=instance.id,
            is_borrowed=False

        )
        loan.save()
        create_card_from_loan(loan)

        instance.loan_link = loan
        instance.save(update_fields=['loan_link'])


@receiver(post_delete, sender=Property)
def delete_property(sender, instance, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    main_properties.properties.remove(instance)


@receiver(post_save, sender=Business)
def create_loan_business(sender, instance, created, **kwargs):
    if created and instance.loan:
        content_type = ContentType.objects.get_for_model(instance)
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.name,
            sum=instance.bought_price,
            loan_term=instance.loan_term,
            percentage=instance.percentage,
            month_payment=instance.month_payment,
            maintenance_cost=instance.month_expense,
            content_type=content_type,
            object_id=instance.id,
            is_borrowed=False

        )
        loan.save()
        create_card_from_loan(loan)

        instance.loan_link = loan
        instance.save(update_fields=['loan_link'])


@receiver(post_delete, sender=Business)
def delete_business(sender, instance, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    main_businesses.businesses.remove(instance)
    actives.save()
    if instance.card:
        instance.card.delete()


@receiver(post_save, sender=Transport)
def create_loan_transport(sender, instance, created, **kwargs):
    if created and instance.loan:
        content_type = ContentType.objects.get_for_model(instance)
        initial_payment = instance.initial_payment or 0
        loan = Loans.objects.create(
            user=instance.user,
            name=instance.mark + instance.model,
            remainder=instance.bought_price - initial_payment,
            sum=instance.bought_price,
            loan_term=instance.loan_term,
            percentage=instance.percentage,
            month_payment=instance.month_payment,
            maintenance_cost=instance.month_expense,
            content_type=content_type,
            object_id=instance.id,
            is_borrowed=False

        )
        loan.save()
        create_card_from_loan(loan)

        instance.loan_link = loan
        instance.save(update_fields=['loan_link'])


@receiver(post_delete, sender=Transport)
def delete_transport(sender, instance, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    main_transport.transport.remove(instance)


@receiver(post_save, sender=Property)
def update_main_properties(sender, instance, created, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    if created:
        main_properties.properties.add(instance)

def create_card_from_loan(loan):
    card = Card.objects.create(
        user=loan.user,
        name=loan.name,
        loan_link=loan,
        from_loan=True,
        percentage=loan.percentage,
        remainder=loan.remainder,
        is_editable=False,  # Карточка создается автоматически и не редактируется пользователем
        is_deletable=False,  # Карточка не удаляется, так как связана с займом
        is_visible=True
    )
    loan.writeoff_account = card
    loan.save(update_fields=['writeoff_account'])
    balance = bal.Balance.objects.get(user=loan.user)
    balance.card_list.add(card)

# Обновление сумм
# Недвижимость
@transaction.atomic
def update_property_totals(sender, instance, created, **kwargs):
    main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_updating_totals'):
        return
    instance._updating_totals = True
    if sender == Property.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        # main_properties.total_income = instance.total_income
    elif sender == Property.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        # main_properties.total_expenses = instance.total_expense
    count_prop_income_expenses(main_properties)
    instance.save(update_fields=['total_income', 'total_expense'])
    # main_properties.save(update_fields=['total_income', 'total_expenses'])
    # actives.save()
    del instance._updating_totals


@transaction.atomic
def count_prop_income_expenses(parent):
    parent.total_income = sum(prop.total_income for prop in parent.properties.all())
    parent.total_expenses = sum(prop.total_expense for prop in parent.properties.all())
    parent.save()


@receiver(m2m_changed, sender=Property.income.through)
@receiver(m2m_changed, sender=Property.expenses.through)
def update_property_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_property_totals(sender=sender, instance=instance, created=False)


@transaction.atomic
def set_mainproperties(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.actual_price for prop in instance.properties.all())
    # instance.save(update_fields=['total_funds'])
    instance.save()
    del instance._count


@receiver(m2m_changed, sender=MainProperties.properties.through)
def set_mainproperties_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_mainproperties(sender=sender, instance=instance, created=False)


# Транспорт
@transaction.atomic
def set_maintransport(sender, instance, created, **kwargs):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True
    instance.total_funds = sum(prop.bought_price for prop in instance.transport.all())
    instance.save(update_fields=['total_funds'])
    del instance._count


@receiver(m2m_changed, sender=MainTransport.transport.through)
def set_maintransport_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        set_maintransport(sender=sender, instance=instance, created=False)


@receiver(post_save, sender=Transport)
def update_main_transport(sender, instance, created, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    if created:
        main_transport.transport.add(instance)


@transaction.atomic
def update_transport_totals(sender, instance, created, **kwargs):
    main_transport = MainTransport.objects.get(user=instance.user)
    actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_updating_totals'):
        return
    instance._updating_totals = True
    if sender == Transport.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        # main_transport.total_income = instance.total_income
    elif sender == Transport.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        # main_transport.total_expenses = instance.total_expense
    instance.save(update_fields=['total_income', 'total_expense'])
    # main_transport.save(update_fields=['total_income', 'total_expenses'])
    count_transport_income_expenses(main_transport)
    # actives.save()
    del instance._updating_totals


@transaction.atomic
def count_transport_income_expenses(parent):
    parent.total_income = sum(prop.total_income for prop in parent.transport.all())
    parent.total_expenses = sum(prop.total_expense for prop in parent.transport.all())
    parent.save()

@receiver(m2m_changed, sender=Transport.income.through)
@receiver(m2m_changed, sender=Transport.expenses.through)
def update_transport_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_transport_totals(sender=sender, instance=instance, created=False)


#  Бизнес
@receiver(post_save, sender=Business)
def update_main_businesses(sender, instance, created, **kwargs):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    # main_loans = MainLoans.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if created:
        main_businesses.businesses.add(instance)

        set_mainbusiness(sender=instance, instance=main_businesses)



@transaction.atomic
def update_business_totals(sender, instance):
    main_businesses = MainBusinesses.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_updating_totals'):
        return
    instance._updating_totals = True
    if sender == Business.income.through:
        instance.total_income = sum(income.funds for income in instance.income.all())
        # main_businesses.total_income = instance.total_income
    elif sender == Business.expenses.through:
        instance.total_expense = sum(expense.funds for expense in instance.expenses.all())
        # main_businesses.total_expenses = instance.total_expense
    # elif sender == Business.equipment.assets:
    #     instance.total_worth = instance.equipment.total_actives_cost
    count_business_income_expenses(main_businesses)
    instance.save(update_fields=['total_income', 'total_expense', 'total_worth'])
    del instance._updating_totals


@transaction.atomic
def count_business_income_expenses(parent):
    parent.total_income = sum(prop.total_income for prop in parent.businesses.all())
    parent.total_expenses = sum(prop.total_expense for prop in parent.businesses.all())
    parent.save()

@receiver(m2m_changed, sender=Business.income.through)
@receiver(m2m_changed, sender=Business.expenses.through)
def update_business_totals_on_income_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear", "post_save"]:
        update_business_totals(sender=sender, instance=instance)


@transaction.atomic
def set_mainbusiness(sender, instance):
    # main_properties = MainProperties.objects.get(user=instance.user)
    # actives = Actives.objects.get(user=instance.user)
    if hasattr(instance, '_count'):
        return
    instance._count = True

    instance.total_funds = sum(prop.total_worth for prop in instance.businesses.all())
    instance.save()
    del instance._count


@receiver(m2m_changed, sender=MainBusinesses.businesses.through)
def set_mainbusiness_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear", "post_save"]:
        set_mainbusiness(sender=sender, instance=instance)


# @receiver(pre_save, sender=InventoryAsset)
# @receiver(pre_delete, sender=InventoryAsset)
# def inventory_asset_changed(sender, instance, **kwargs):
#     if hasattr(instance, 'inventory') and instance.inventory:
#         inventory = instance.inventory
#         if inventory.content_type and inventory.content_type.model == 'business':
#             business_instance = inventory.content_type.get_object_for_this_type(id=inventory.object_id)
#             update_business_totals(sender=Business.equipment.assets, instance=business_instance)


@transaction.atomic
def count_actives(sender, instance):
    actives = Actives.objects.get(user=instance.user)
    total_funds = 0
    total_income = 0
    total_expenses = 0
    if actives.properties:
        total_funds += actives.properties.total_funds or 0
        total_income += actives.properties.total_income or 0
        total_expenses += actives.properties.total_expenses or 0
    if actives.transports:
        total_funds += actives.transports.total_funds or 0
        total_income += actives.transports.total_income or 0
        total_expenses += actives.transports.total_expenses or 0
    if actives.businesses:
        total_funds += actives.businesses.total_funds or 0
        total_income += actives.businesses.total_income or 0
        total_expenses += actives.businesses.total_expenses or 0
    if actives.securities:
        total_funds += actives.securities.total_funds or 0
        total_income += actives.securities.total_income or 0
        total_expenses += actives.securities.total_expenses or 0
    if actives.jewelries:
        total_funds += actives.jewelries.total_funds or 0
        total_income += actives.jewelries.total_income or 0
        total_expenses += actives.jewelries.total_expenses or 0
    if actives.deposits:
        total_funds += actives.deposits.total_funds or 0
        total_income += actives.deposits.total_income or 0
        total_expenses += actives.deposits.total_expenses or 0

    actives.total_funds = total_funds
    actives.total_income = total_income
    actives.total_expenses = total_expenses
    actives.save()


@receiver(post_save, sender=MainProperties)
@receiver(post_save, sender=MainBusinesses)
@receiver(post_save, sender=MainTransport)
@receiver(post_save, sender=MainSecurities)
@receiver(post_save, sender=MainJewelry)
@receiver(post_save, sender=MainDeposits)
def set_actives(sender, instance, **kwargs):
    count_actives(sender, instance)


@receiver(post_save, sender=Property)
def property_post_save(sender, instance, created, **kwargs):
    if created:
        src = 'actives'


@receiver(post_delete, sender=ActivesIncome)
@receiver(post_delete, sender=ActivesExpenses)
def delete_child(sender, instance, **kwargs):
    instance.child.delete()