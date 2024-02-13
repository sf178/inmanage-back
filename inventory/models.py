from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from front.models import CustomUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from front.models import CustomUser


class PreviousInventoryAsset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    added = models.BooleanField(default=False, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    flag = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"InventoryAsset {self.id} - {self.user.username}"


class PreviousInventory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    category_object = GenericForeignKey('content_type', 'object_id')
    assets = models.ManyToManyField('inventory.PreviousInventoryAsset', related_name='+', blank=True)
    launch_status = models.BooleanField(default=False, null=True, blank=True)
    expenses = models.ManyToManyField('inventory.InventoryExpenses', blank=True, related_name='+')
    total_cost = models.FloatField(default=0.0, null=True, blank=True)
    previous_inventory = GenericRelation('self', related_query_name='+', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InventoryAsset(models.Model):
    id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    added = models.BooleanField(default=False, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    flag = models.BooleanField(default=False, null=True, blank=True)
    is_consumables = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"InventoryAsset {self.id} - {self.user}"

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    category_object = GenericForeignKey('content_type', 'object_id')
    assets = models.ManyToManyField(InventoryAsset, related_name='+', blank=True)
    launch_status = models.BooleanField(default=False, null=True, blank=True)
    expenses = models.ManyToManyField('inventory.InventoryExpenses', blank=True, related_name='+')
    total_cost = models.FloatField(default=0.0, null=True, blank=True)
    previous_inventories = models.ManyToManyField('inventory.PreviousInventory', related_name='+',
                                                  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventory {self.id} - {self.user.username}"


class InventoryExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('front.CustomUser', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    writeoff_account = models.ForeignKey('balance.Card', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    category = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    funds = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)