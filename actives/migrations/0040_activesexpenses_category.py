# Generated by Django 4.1.7 on 2023-08-12 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0039_alter_business_expenses_alter_business_income_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activesexpenses',
            name='category',
            field=models.TextField(blank=True),
        ),
    ]