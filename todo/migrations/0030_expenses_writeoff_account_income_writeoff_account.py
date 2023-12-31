# Generated by Django 4.1.7 on 2023-08-12 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0013_expenses_category'),
        ('todo', '0029_expenses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='writeoff_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='balance.card'),
        ),
        migrations.AddField(
            model_name='income',
            name='writeoff_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='balance.card'),
        ),
    ]
