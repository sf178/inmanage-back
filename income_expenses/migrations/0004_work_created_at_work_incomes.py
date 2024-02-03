# Generated by Django 4.1.7 on 2024-02-03 00:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('income_expenses', '0003_workincome_child_delete_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='work',
            name='incomes',
            field=models.ManyToManyField(blank=True, null=True, related_name='+', to='income_expenses.workincome'),
        ),
    ]