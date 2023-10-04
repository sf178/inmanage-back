# Generated by Django 4.1.7 on 2023-09-02 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0009_previousinventoryasset_and_more'),
        ('passives', '0035_expenses_writeoff_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='property',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='inventory.inventory'),
        ),
        migrations.AlterField(
            model_name='property',
            name='loan_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='passives.loans'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='loan_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='passives.loans'),
        ),
    ]
