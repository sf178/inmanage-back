from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from front.models import CustomUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from front.models import CustomUser


class InventoryAsset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    added = models.BooleanField(default=False, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    flag = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"InventoryAsset {self.id} - {self.user.username}"

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    category_object = GenericForeignKey('content_type', 'object_id')
    assets = models.ManyToManyField(InventoryAsset, related_name='assets', blank=True)
    launch_status = models.BooleanField(default=False, null=True, blank=True)
    total_cost = models.FloatField(default=0.0, null=True, blank=True)
    previous_inventories = GenericRelation('self', related_query_name='previous_inventory', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventory {self.id} - {self.user.username}"
