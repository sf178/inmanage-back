# Generated by Django 4.1.6 on 2023-07-31 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0022_alter_transport_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actives',
            name='bonds',
        ),
        migrations.RemoveField(
            model_name='actives',
            name='stocks',
        ),
    ]
