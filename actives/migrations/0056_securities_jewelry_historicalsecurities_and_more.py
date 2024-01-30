# Generated by Django 4.1.7 on 2024-01-25 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actives', '0055_activesexpenses_child_activesincome_child'),
    ]

    operations = [
        migrations.CreateModel(
            name='Securities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('broker', models.TextField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('market_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Jewelry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('purchase_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('estimated_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='jewelry_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalSecurities',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('broker', models.TextField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('market_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical securities',
                'verbose_name_plural': 'historical securitiess',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalJewelry',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('purchase_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('estimated_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical jewelry',
                'verbose_name_plural': 'historical jewelrys',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]