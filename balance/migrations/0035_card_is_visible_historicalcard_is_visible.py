# Generated by Django 4.1.7 on 2024-03-17 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0034_alter_card_is_editable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalcard',
            name='is_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
