# Generated by Django 4.1.6 on 2023-06-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0018_alter_todoitem_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todotask',
            name='done',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
