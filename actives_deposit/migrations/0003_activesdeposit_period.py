# Generated by Django 4.1.7 on 2024-02-12 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives_deposit', '0002_activesdeposit_incomes'),
    ]

    operations = [
        migrations.AddField(
            model_name='activesdeposit',
            name='period',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
