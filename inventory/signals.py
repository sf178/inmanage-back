from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver
from django.db.models import Sum

from actives.models import Business
from .models import InventoryAsset, Inventory
from django.contrib.contenttypes.models import ContentType


@receiver(pre_delete, sender=InventoryAsset)
def update_inventory_total_cost_before_delete(sender, instance, **kwargs):
    """
    Обрабатывает удаление активов инвентаря и обновляет total_cost инвентаря и total_worth связанного бизнеса.
    """
    inventory = Inventory.objects.filter(assets=instance).first()
    if inventory:
        inventory.total_cost -= instance.price
        inventory.save()
        if inventory.content_type.model_class() == Business:
            business_instance = inventory.content_type.get_object_for_this_type(id=inventory.object_id)
            calculate_total_worth(business_instance)

@receiver(m2m_changed, sender=Inventory.assets.through)
def recalculate_inventory_total_cost(sender, instance, action, **kwargs):
    """
    Обрабатывает изменения в assets инвентаря и пересчитывает total_cost инвентаря и total_worth связанного бизнеса.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.total_cost = sum(asset.price for asset in instance.assets.all())
        instance.save()
        if instance.content_type.model_class() == Business:
            business_instance = instance.content_type.get_object_for_this_type(id=instance.object_id)
            calculate_total_worth(business_instance)

def update_business_total_worth(business_instance):
    # Обновление total_worth для Business, если необходимо
    business_instance.total_worth = business_instance.calculate_total_worth()  # Предполагается, что метод calculate_total_worth() существует
    business_instance.save()


def update_related_business_total_worth(inventory):
    if inventory.content_type and inventory.object_id:
        business_model = inventory.content_type.model_class()
        if issubclass(business_model, Business):
            business_instance = business_model.objects.get(id=inventory.object_id)
            update_business_total_worth(business_instance)


def calculate_total_worth(business_instance):
    """
    Пересчитывает и обновляет total_worth для объекта Business на основе его revenue и общей стоимости инвентаря.
    """
    inventory_total_cost = Inventory.objects.filter(
        content_type=ContentType.objects.get_for_model(Business),
        object_id=business_instance.id
    ).aggregate(total_cost_sum=Sum('total_cost'))['total_cost_sum'] or 0

    # Суммируем revenue бизнеса и общую стоимость инвентаря
    total_worth = business_instance.revenue + inventory_total_cost
    business_instance.total_worth = total_worth
    business_instance.save()