# Generated by Django 4.1.7 on 2023-08-09 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0035_business_bought_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bonds',
        ),
        migrations.RemoveField(
            model_name='businessasset',
            name='business',
        ),
        migrations.RemoveField(
            model_name='historicalbusinessasset',
            name='business',
        ),
        migrations.RemoveField(
            model_name='historicalbusinessasset',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpropertyasset',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpropertyasset',
            name='property',
        ),
        migrations.RemoveField(
            model_name='propertyasset',
            name='property',
        ),
        migrations.RemoveField(
            model_name='securities',
            name='user',
        ),
        migrations.DeleteModel(
            name='Stocks',
        ),
    ]
