# Generated by Django 4.1.6 on 2023-05-31 21:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0004_loans_loan_term_alter_loans_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loans',
            name='data',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
