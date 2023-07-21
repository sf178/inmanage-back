# Generated by Django 4.1.6 on 2023-05-31 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0008_objectsprofile_remove_card_card_cvc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='loan',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='loan',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='loan',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='rent_type',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
