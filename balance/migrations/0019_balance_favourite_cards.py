# Generated by Django 4.1.7 on 2023-10-04 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0018_rename_total_expenses_card_total_expense_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='favourite_cards',
            field=models.ManyToManyField(blank=True, null=True, related_name='+', to='balance.card'),
        ),
    ]