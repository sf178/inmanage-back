# Generated by Django 4.1.7 on 2023-10-07 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_expensegeneralcategory_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensegeneralcategory',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expensepersonalcategory',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
