# Generated by Django 4.1.7 on 2024-03-26 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0036_card_loan_link_historicalcard_loan_link_and_more'),
        ('todo', '0038_historicaltodotask_amount_todotask_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltodotask',
            name='child',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='balance.payment'),
        ),
        migrations.AddField(
            model_name='todotask',
            name='child',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='balance.payment'),
        ),
    ]
