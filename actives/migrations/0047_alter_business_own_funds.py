# Generated by Django 4.1.7 on 2023-12-02 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0046_alter_business_address_alter_business_creditor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='own_funds',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]