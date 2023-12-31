# Generated by Django 4.1.7 on 2023-08-09 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0026_expenses_loan_loans_expenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passives',
            name='loans',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.mainloans'),
        ),
        migrations.AlterField(
            model_name='passives',
            name='properties',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.mainproperties'),
        ),
        migrations.AlterField(
            model_name='passives',
            name='transports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='passives.maintransport'),
        ),
    ]
