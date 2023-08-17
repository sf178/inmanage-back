# Generated by Django 4.1.7 on 2023-08-17 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0043_alter_activesexpenses_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesexpenses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='activesincome',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='historicalbusiness',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='historicalproperty',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='historicaltransport',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
