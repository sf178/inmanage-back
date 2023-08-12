# Generated by Django 4.1.7 on 2023-08-12 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventoryasset_text_alter_inventory_created_at_and_more'),
        ('passives', '0031_alter_expenses_funds_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproperty',
            name='equipment',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='property',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='inventory.inventory'),
        ),
    ]
