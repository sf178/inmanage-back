# Generated by Django 4.1.7 on 2024-01-04 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0021_income_writeoff_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
