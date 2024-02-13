# Generated by Django 4.1.7 on 2024-02-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0029_remove_historicalpayment_is_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpayment',
            name='is_paid',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]