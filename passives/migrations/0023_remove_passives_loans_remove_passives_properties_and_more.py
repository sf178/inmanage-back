# Generated by Django 4.1.7 on 2023-08-07 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('passives', '0022_alter_historicalloans_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passives',
            name='loans',
        ),
        migrations.RemoveField(
            model_name='passives',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='passives',
            name='transports',
        ),
        migrations.CreateModel(
            name='MainTransport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_funds', models.FloatField(blank=True, null=True)),
                ('total_expenses', models.FloatField(blank=True, null=True)),
                ('transport', models.ManyToManyField(blank=True, to='passives.transport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainProperties',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_funds', models.FloatField(blank=True, null=True)),
                ('total_expenses', models.FloatField(blank=True, null=True)),
                ('properties', models.ManyToManyField(blank=True, to='passives.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainLoans',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_funds', models.FloatField(blank=True, null=True)),
                ('total_expenses', models.FloatField(blank=True, null=True)),
                ('loans', models.ManyToManyField(blank=True, to='passives.loans')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='passives',
            name='loans',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.maintransport'),
        ),
        migrations.AddField(
            model_name='passives',
            name='properties',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.mainproperties'),
        ),
        migrations.AddField(
            model_name='passives',
            name='transports',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.maintransport'),
        ),
    ]