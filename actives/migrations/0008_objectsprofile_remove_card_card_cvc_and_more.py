# Generated by Django 4.1.6 on 2023-05-26 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('passives', '0003_alter_loans_data_alter_loans_insurance_and_more'),
        ('actives', '0007_rename_business_id_businessasset_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectsProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'ordering': ('id',),
            },
        ),
        migrations.RemoveField(
            model_name='card',
            name='card_cvc',
        ),
        migrations.AlterField(
            model_name='actives',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='HIGH',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='LOW',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='MARKETPRICE2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='MARKETPRICE3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='OPEN',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='average_profit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='creditor',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='direction',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='loan_sum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='loan_term',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='month_expense',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='month_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='month_payment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='own_funds',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='revenue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='third_party_tools',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='third_party_tools_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='type',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='businessasset',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actives.business'),
        ),
        migrations.AlterField(
            model_name='businessasset',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businessasset',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propertyasset',
            name='property_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actives.property'),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='HIGH',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='LOW',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='OPEN',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='SHORTNAME',
            field=models.TextField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transport',
            name='average_profit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='bought_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='brand',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='initial_payment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='loan_term',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='month_expense',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='month_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='month_payment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='owner',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='owner_type',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='revenue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='use',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='objectsprofile',
            name='actives',
            field=models.ManyToManyField(blank=True, to='actives.actives'),
        ),
        migrations.AddField(
            model_name='objectsprofile',
            name='cards',
            field=models.ManyToManyField(blank=True, to='actives.card'),
        ),
        migrations.AddField(
            model_name='objectsprofile',
            name='passives',
            field=models.ManyToManyField(blank=True, to='passives.passives'),
        ),
        migrations.AddField(
            model_name='objectsprofile',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
