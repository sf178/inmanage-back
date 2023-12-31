# Generated by Django 4.1.7 on 2023-08-17 21:07

import actives.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0042_activesexpenses_description_activesexpenses_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesexpenses',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='activesincome',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historicalbusiness',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalproperty',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaltransport',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='created_at',
            field=actives.models.MillisecondDateTimeField(auto_now_add=True),
        ),
    ]
