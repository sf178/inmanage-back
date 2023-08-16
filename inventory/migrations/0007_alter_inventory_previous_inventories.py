# Generated by Django 4.1.7 on 2023-08-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_previousinventory_inventory_previous_inventories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='previous_inventories',
            field=models.ManyToManyField(blank=True, null=True, related_name='previous_inventory', to='inventory.previousinventory'),
        ),
    ]
