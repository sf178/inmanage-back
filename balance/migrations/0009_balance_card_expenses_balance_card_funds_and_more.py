# Generated by Django 4.1.7 on 2023-08-07 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0008_alter_balance_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='card_expenses',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='card_funds',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalbalance',
            name='card_expenses',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalbalance',
            name='card_funds',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
