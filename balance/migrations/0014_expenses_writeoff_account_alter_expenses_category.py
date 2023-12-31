# Generated by Django 4.1.7 on 2023-08-14 02:32

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0013_expenses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='writeoff_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='balance.card'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, default=list, size=None),
        ),
    ]
