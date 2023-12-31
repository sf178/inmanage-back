# Generated by Django 4.1.6 on 2023-05-01 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('data', models.CharField(max_length=255)),
                ('insurance', models.BooleanField(default=False)),
                ('insurance_sum', models.FloatField(default=0)),
                ('remainder', models.FloatField()),
                ('sum', models.FloatField()),
                ('percentage', models.FloatField()),
                ('month_payment', models.FloatField()),
                ('maintenance_cost', models.FloatField()),
            ],
            options={
                'verbose_name': 'loan',
                'verbose_name_plural': 'loans',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Passives',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField()),
                ('properties', models.TextField()),
                ('transports', models.TextField()),
                ('loans', models.TextField()),
            ],
            options={
                'verbose_name': 'passives',
                'verbose_name_plural': 'passives',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField()),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('owner', models.TextField()),
                ('rent_type', models.BooleanField()),
                ('bought_price', models.FloatField()),
                ('actual_price', models.FloatField()),
                ('initial_payment', models.FloatField()),
                ('loan_term', models.FloatField()),
                ('percentage', models.FloatField()),
                ('month_payment', models.FloatField()),
                ('equipment_price', models.FloatField()),
                ('month_income', models.FloatField()),
                ('month_expense', models.FloatField()),
                ('average_consumption', models.FloatField()),
            ],
            options={
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField()),
                ('brand', models.TextField()),
                ('name', models.TextField()),
                ('owner', models.TextField()),
                ('owner_type', models.BooleanField()),
                ('vin', models.CharField(max_length=17)),
                ('use', models.TextField()),
                ('bought_price', models.FloatField()),
                ('initial_payment', models.FloatField()),
                ('loan_term', models.FloatField()),
                ('percentage', models.FloatField()),
                ('month_payment', models.FloatField()),
                ('month_expense', models.FloatField()),
                ('average_consumption', models.FloatField()),
            ],
            options={
                'verbose_name': 'transport',
                'verbose_name_plural': 'transport',
                'ordering': ('id',),
            },
        ),
    ]
