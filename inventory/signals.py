from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from actives.models import Business
from .models import InventoryAsset, Inventory
from django.contrib.contenttypes.models import ContentType


@receiver(m2m_changed, sender=Inventory.assets.through)
def recalculate_inventory_total_cost(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        total_cost = sum(asset.price for asset in instance.assets.all())
        instance.total_cost = total_cost
        instance.save()

        if instance.inventory.content_type and instance.inventory.object_id:
            business_model = instance.inventory.content_type.model_class()
            if issubclass(business_model, Business):
                business_instance = business_model.objects.get(id=instance.inventory.object_id)
                update_business_total_worth(business_instance)

def update_business_total_worth(business_instance):
    # Обновление total_worth для Business, если необходимо
    business_instance.total_worth = business_instance.calculate_total_worth()  # Предполагается, что метод calculate_total_worth() существует
    business_instance.save()
