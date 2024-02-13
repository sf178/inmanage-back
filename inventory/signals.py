from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import InventoryAsset, Inventory
from actives.models import Business
from django.contrib.contenttypes.models import ContentType


# @receiver(post_save, sender=InventoryAsset)
# @receiver(post_delete, sender=InventoryAsset)
@receiver(pre_delete, sender=InventoryAsset)
@receiver(pre_save, sender=InventoryAsset)
def update_inventory_total_cost(sender, instance, **kwargs):
    # Предположим, что у InventoryAsset есть ForeignKey к Inventory
    inventory = instance.inventory
    if inventory:
        total_cost = sum(asset.price for asset in inventory.assets.all())
        inventory.total_cost = total_cost
        inventory.save()
        # Вызов функции обновления total_worth для связанного бизнеса
        update_business_total_worth(inventory)




def update_business_total_worth(inventory):
    if inventory.content_type and inventory.object_id:
        business_model = inventory.content_type.model_class()
        if issubclass(business_model, Business):
            business_instance = business_model.objects.get(id=inventory.object_id)
            business_instance.total_worth = calculate_business_total_worth(business_instance)
            business_instance.save()


def calculate_business_total_worth(business_instance):
    # Пересчёт total_worth для бизнеса
    inventory = business_instance.equipment
    worth = business_instance.revenue + inventory.total_cost
    # Предположим, что revenue уже есть в бизнесе
    return worth
