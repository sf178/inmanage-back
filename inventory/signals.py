from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import InventoryAsset, Inventory
from actives.models import Business
from django.contrib.contenttypes.models import ContentType

@receiver(pre_delete, sender=InventoryAsset)
def update_inventory_total_cost_before_delete(sender, instance, **kwargs):
    # Проверяем, связан ли asset с каким-либо инвентарем
    inventory = Inventory.objects.filter(assets=instance).first()
    if inventory:
        # Вычитаем стоимость удаляемого asset из total_cost инвентаря
        inventory.total_cost -= instance.price
        inventory.save()
        # Пересчитываем total_worth для связанного бизнеса, если есть
        update_business_total_worth(inventory)

@receiver(m2m_changed, sender=Inventory.assets.through)
def recalculate_inventory_total_cost(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        total_cost = sum(asset.price for asset in instance.assets.all())
        instance.total_cost = total_cost
        instance.save()

        if instance.content_type and instance.object_id:
            business_model = instance.content_type.model_class()
            if issubclass(business_model, Business):
                business_instance = business_model.objects.get(id=instance.object_id)
                update_business_total_worth(business_instance)

# @receiver(post_save, sender=InventoryAsset)
# @receiver(post_delete, sender=InventoryAsset)
@receiver(pre_delete, sender=InventoryAsset)
@receiver(pre_save, sender=InventoryAsset)
def update_inventory_total_cost(sender, instance, **kwargs):
    # Предположим, что у InventoryAsset есть ForeignKey к Inventory
    inventory = instance.inventory
    if inventory:
        inventory = Inventory.objects.get(pk=instance.inventory.pk)
        inventory.total_cost = sum(asset.price for asset in inventory.assets.all())
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
