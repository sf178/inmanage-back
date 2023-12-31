# Generated by Django 4.1.6 on 2023-06-27 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bank', models.BooleanField(blank=True, null=True)),
                ('bank_name', models.TextField(blank=True, default=None, null=True)),
                ('card_num', models.TextField(blank=True, default=None, max_length=16, null=True)),
                ('loan', models.BooleanField(blank=True, null=True)),
                ('interest_free', models.IntegerField(blank=True, default=None, null=True)),
                ('percentage', models.IntegerField(blank=True, default=None, null=True)),
                ('balance', models.IntegerField(blank=True, default=None, null=True)),
                ('limit', models.IntegerField(blank=True, default=None, null=True)),
                ('flag', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'card',
                'verbose_name_plural': 'cards',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('total_in_currency', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
