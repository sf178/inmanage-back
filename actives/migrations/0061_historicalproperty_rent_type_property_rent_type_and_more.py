# Generated by Django 4.1.7 on 2024-02-12 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0060_remove_historicalproperty_rent_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproperty',
            name='rent_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='rent_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalproperty',
            name='owner',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.TextField(blank=True, null=True),
        ),
    ]
