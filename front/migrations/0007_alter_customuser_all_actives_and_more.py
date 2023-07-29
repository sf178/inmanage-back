# Generated by Django 4.1.6 on 2023-07-31 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0024_business_expenses_business_income_expenses_user_and_more'),
        ('passives', '0019_rename_user_id_passives_user_property_expenses_and_more'),
        ('todo', '0024_alter_historicalproject_writeoff_account_and_more'),
        ('front', '0006_alter_customuser_all_actives_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='all_actives',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='actives.actives'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='all_passives',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='passives.passives'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='all_plans',
            field=models.ManyToManyField(blank=True, null=True, to='todo.planner'),
        ),
    ]
