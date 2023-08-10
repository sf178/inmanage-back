# Generated by Django 4.1.7 on 2023-08-07 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0021_historicalproperty_loan_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalloans',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicalloans',
            name='maintenance_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalloans',
            name='month_payment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalloans',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalloans',
            name='remainder',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalloans',
            name='sum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bank_images/'),
        ),
        migrations.AlterField(
            model_name='loans',
            name='maintenance_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='month_payment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='remainder',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='sum',
            field=models.FloatField(blank=True, null=True),
        ),
    ]