# Generated by Django 4.1.7 on 2023-12-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0051_activesincome_comment_activesincome_writeoff_account_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproperty',
            name='address',
        ),
        migrations.RemoveField(
            model_name='property',
            name='address',
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='building_number',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='square',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='street',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='building_number',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='property',
            name='city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='square',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='street',
            field=models.TextField(blank=True, null=True),
        ),
    ]