# Generated by Django 4.1.7 on 2023-12-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_previousinventoryasset_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryasset',
            name='is_consumables',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
