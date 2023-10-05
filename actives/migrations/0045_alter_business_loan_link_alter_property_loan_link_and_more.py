# Generated by Django 4.1.7 on 2023-09-02 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0035_expenses_writeoff_account'),
        ('actives', '0044_alter_activesexpenses_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='loan_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='passives.loans'),
        ),
        migrations.AlterField(
            model_name='property',
            name='loan_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_loan_link', to='passives.loans'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='loan_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='passives.loans'),
        ),
    ]