# Generated by Django 4.1.6 on 2023-05-26 12:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_remove_todotask_date_project_planned_sum_and_more'),
        ('passives', '0003_alter_loans_data_alter_loans_insurance_and_more'),
        ('actives', '0008_objectsprofile_remove_card_card_cvc_and_more'),
        ('front', '0002_alter_customuser_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active_objects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(null=True), blank=True, default=[], size=None),
        ),
        migrations.AddField(
            model_name='customuser',
            name='all_actives',
            field=models.ManyToManyField(blank=True, to='actives.actives'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='all_passives',
            field=models.ManyToManyField(blank=True, to='passives.passives'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='all_plans',
            field=models.ManyToManyField(blank=True, to='todo.planner'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deleted_objects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(null=True), blank=True, default=[], size=None),
        ),
    ]
