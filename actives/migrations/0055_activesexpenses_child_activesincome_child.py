# Generated by Django 4.1.7 on 2024-01-08 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0023_remove_expenses_card_remove_income_card_and_more'),
        ('actives', '0054_remove_activesexpenses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='activesexpenses',
            name='child',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='balance.expenses'),
        ),
        migrations.AddField(
            model_name='activesincome',
            name='child',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='balance.income'),
        ),
    ]