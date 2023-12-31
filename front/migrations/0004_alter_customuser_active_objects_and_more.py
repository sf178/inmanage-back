# Generated by Django 4.1.6 on 2023-05-26 12:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_customuser_active_objects_customuser_all_actives_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='active_objects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(null=True), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='deleted_objects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(null=True), blank=True, default=list, size=None),
        ),
    ]
