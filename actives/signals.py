from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .serializers import *


@receiver(post_save, sender=Property)
@receiver(post_delete, sender=Property)
@receiver(post_save, sender=Transport)
@receiver(post_delete, sender=Transport)
@receiver(post_save, sender=Business)
@receiver(post_delete, sender=Business)
@receiver(post_save, sender=Stocks)
@receiver(post_delete, sender=Stocks)
@receiver(post_save, sender=Bonds)
@receiver(post_delete, sender=Bonds)
def update_actives(sender, instance, **kwargs):
    user_id = instance.user_id
    active, created = Actives.objects.get_or_create(user_id=user_id)
    if isinstance(instance, Property):
        active.properties.set(Property.objects.filter(user_id=user_id))
    elif isinstance(instance, Transport):
        active.transports.set(Transport.objects.filter(user_id=user_id))
    elif isinstance(instance, Business):
        active.businesses.set(Business.objects.filter(user_id=user_id))
    elif isinstance(instance, Stocks):
        active.stocks.set(Stocks.objects.filter(user_id=user_id))
    elif isinstance(instance, Bonds):
        active.obligation.set(Bonds.objects.filter(user_id=user_id))
