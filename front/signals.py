from django.db.models.signals import post_save
from django.dispatch import receiver
import balance.models as bal
import actives.models as act
import passives.models as pas
import todo.models as todo
from .models import UserProfile
from front.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_balance(sender, instance, created, **kwargs):
    if created:
        balance = bal.Balance.objects.create(user=instance)
        card = bal.Card.objects.create(user=instance, name='Наличный счет', bank=False, loan=False, currency='RUB', )
        balance.card_list.add(card)
        balance.save()
        instance.balance = balance
        instance.save()


@receiver(post_save, sender=CustomUser)
def create_actives(sender, instance, created, **kwargs):
    if created:
        actives = act.Actives.objects.create(user=instance)
        main_properties, _ = act.MainProperties.objects.get_or_create(user=instance)
        main_transport, _ = act.MainTransport.objects.get_or_create(user=instance)
        main_businesses, _ = act.MainBusinesses.objects.get_or_create(user=instance)
        main_jewelries, _ = act.MainJewelry.objects.get_or_create(user=instance)
        main_securities, _ = act.MainSecurities.objects.get_or_create(user=instance)
        # main_loans, _ = act.MainLoans.objects.get_or_create(user=instance)
        main_deposits, _ = act.MainDeposits.objects.get_or_create(user=instance)
        actives.properties = main_properties
        actives.transports = main_transport
        actives.businesses = main_businesses
        actives.jewelries = main_jewelries
        actives.securities = main_securities
        # actives.loans = main_loans
        actives.deposits = main_deposits
        actives.save(update_fields=['properties', 'transports', 'businesses', 'jewelries', 'securities', 'deposits'])
        instance.all_actives = actives
        instance.save()


@receiver(post_save, sender=CustomUser)
def create_passives(sender, instance, created, **kwargs):
    if created:
        passives = pas.Passives.objects.create(user=instance)
        main_properties, _ = pas.MainProperties.objects.get_or_create(user=instance)
        main_transport, _ = pas.MainTransport.objects.get_or_create(user=instance)
        main_loans, _ = pas.MainLoans.objects.get_or_create(user=instance)
        passives.properties = main_properties
        passives.transports = main_transport
        passives.loans = main_loans
        passives.save(update_fields=['properties', 'transports', 'loans'])
        instance.all_passives = passives
        instance.save()


@receiver(post_save, sender=CustomUser)
def create_planner(sender, instance, created, **kwargs):
    if created:
        planner = todo.Planner.objects.create(user=instance)
        task = todo.TodoTask.objects.create(user=instance, title='Список дел')
        planner.tasks.add(task)
        planner.save()
        