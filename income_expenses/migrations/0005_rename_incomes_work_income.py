# Generated by Django 4.1.7 on 2024-02-03 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income_expenses', '0004_work_created_at_work_incomes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='incomes',
            new_name='income',
        ),
    ]