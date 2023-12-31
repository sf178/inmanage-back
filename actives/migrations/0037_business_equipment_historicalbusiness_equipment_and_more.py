# Generated by Django 4.1.7 on 2023-08-09 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0036_delete_bonds_remove_businessasset_business_and_more'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='historicalbusiness',
            name='equipment',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='equipment',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='property',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='inventory.inventory'),
        ),
        migrations.DeleteModel(
            name='BusinessAsset',
        ),
        migrations.DeleteModel(
            name='HistoricalBusinessAsset',
        ),
        migrations.DeleteModel(
            name='HistoricalPropertyAsset',
        ),
        migrations.DeleteModel(
            name='PropertyAsset',
        ),
        migrations.DeleteModel(
            name='Securities',
        ),
    ]
