# Generated by Django 4.1.6 on 2023-06-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0013_alter_project_date_end_alter_project_date_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todotask',
            name='done',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
