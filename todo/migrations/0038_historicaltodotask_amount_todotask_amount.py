# Generated by Django 4.1.7 on 2024-03-26 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0037_expenses_child_income_child'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltodotask',
            name='amount',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='todotask',
            name='amount',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
