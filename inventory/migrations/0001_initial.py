# Generated by Django 4.1.7 on 2023-08-09 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryAsset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('added', models.BooleanField(blank=True, default=False, null=True)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('flag', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('launch_status', models.BooleanField(blank=True, default=False, null=True)),
                ('total_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('assets', models.ManyToManyField(blank=True, related_name='assets', to='inventory.inventoryasset')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]