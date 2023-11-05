from django.db import models


class Receipt(models.Model):
    date_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_inn = models.CharField(max_length=255, null=True, blank=True)
    retail_place_address = models.CharField(max_length=255, null=True, blank=True)
    shift_number = models.PositiveIntegerField(null=True, blank=True)
    taxation_type = models.PositiveIntegerField(null=True, blank=True)
    electronic_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fiscal_sign = models.PositiveIntegerField(null=True, blank=True)
    request_number = models.PositiveIntegerField(null=True, blank=True)
    fiscal_document_number = models.PositiveIntegerField(null=True, blank=True)
    fiscal_document_format_version = models.PositiveIntegerField(null=True, blank=True)
    fiscal_drive_number = models.CharField(max_length=255, null=True, blank=True)
    kkt_registration_id = models.CharField(max_length=255, null=True, blank=True)
    operation_type = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Receipt'
        verbose_name_plural = 'Receipts'


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    item_number = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nds = models.PositiveIntegerField(null=True, blank=True)
    payment_type = models.PositiveIntegerField(null=True, blank=True)
    product_type = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Receipt Item'
        verbose_name_plural = 'Receipt Items'
