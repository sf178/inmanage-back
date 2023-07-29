from django.db.models.signals import post_save
from django.dispatch import receiver
from balance.models import Balance
from actives.models import Actives
from passives.models import Passives

from front.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_balance(sender, instance, created, **kwargs):
    if created:
        balance = Balance.objects.create(user=instance)
        instance.balance = balance
        instance.save()


@receiver(post_save, sender=CustomUser)
def create_actives(sender, instance, created, **kwargs):
    if created:
        actives = Actives.objects.create(user=instance)
        instance.all_actives = actives
        instance.save()


@receiver(post_save, sender=CustomUser)
def create_passives(sender, instance, created, **kwargs):
    if created:
        passives = Passives.objects.create(user=instance)
        instance.all_passives = passives
        instance.save()
