# Generated by Django 4.1.7 on 2023-08-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0009_balance_card_expenses_balance_card_funds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='card_list',
            field=models.ManyToManyField(blank=True, null=True, to='balance.card'),
        ),
    ]
