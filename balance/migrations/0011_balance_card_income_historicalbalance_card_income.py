# Generated by Django 4.1.7 on 2023-08-09 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0010_alter_balance_card_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='card_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalbalance',
            name='card_income',
            field=models.FloatField(blank=True, null=True),
        ),
    ]