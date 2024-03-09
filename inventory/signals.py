from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import InventoryAsset, Inventory
from actives.models import Business
from django.contrib.contenttypes.models import ContentType


@receiver(post_delete, sender=InventoryAsset)
def update_inventory_total_cost_before_delete(sender, instance, **kwargs):
    # Проверяем, связан ли asset с каким-либо инвентарем
    inventory = Inventory.objects.filter(assets=instance).first()
    if inventory:
        # Вычитаем стоимость удаляемого asset из total_actives_cost инвентаря
        instance.total_actives_cost = sum(
            (asset.price * asset.count) for asset in instance.assets.all() if not asset.is_consumables)
        instance.total_consumables_cost = sum(
            (asset.price * asset.count) for asset in instance.assets.all() if asset.is_consumables)

    # Пересчитываем total_worth для связанного бизнеса, если есть



@receiver(m2m_changed, sender=Inventory.assets.through)
def recalculate_inventory_total_cost(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear", "post_save"]:
        instance.total_actives_cost = sum((asset.price * asset.count) for asset in instance.assets.all() if not asset.is_consumables)
        instance.total_consumables_cost = sum((asset.price * asset.count) for asset in instance.assets.all() if asset.is_consumables)

        instance.save()

        business_instance = Business.objects.get(id=instance.object_id)
        business_instance.total_worth = instance.total_actives_cost
        business_instance.save()


@receiver(post_delete, sender=InventoryAsset)
@receiver(pre_save, sender=InventoryAsset)
def update_inventory_total_cost(sender, instance, **kwargs):
    # Предположим, что у InventoryAsset есть ForeignKey к Inventory
    inventory = instance.inventory
    if inventory:
        inventory = Inventory.objects.get(pk=instance.inventory.pk)
        inventory.total_actives_cost = sum(asset.price for asset in inventory.assets.all() if not asset.is_consumables)
        inventory.total_consumables_cost = sum(asset.price for asset in inventory.assets.all() if asset.is_consumables)
        inventory.save()


