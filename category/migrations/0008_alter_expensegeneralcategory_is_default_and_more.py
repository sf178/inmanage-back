# Generated by Django 4.1.7 on 2023-10-08 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_expensegeneralcategory_is_default_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensegeneralcategory',
            name='is_default',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='expensepersonalcategory',
            name='is_default',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
