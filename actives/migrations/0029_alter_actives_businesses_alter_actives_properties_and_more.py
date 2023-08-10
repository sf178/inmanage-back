# Generated by Django 4.1.7 on 2023-08-07 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actives', '0028_remove_actives_businesses_remove_actives_properties_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actives',
            name='businesses',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='actives.mainbusinesses'),
        ),
        migrations.AlterField(
            model_name='actives',
            name='properties',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='actives.mainproperties'),
        ),
        migrations.AlterField(
            model_name='actives',
            name='transports',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='actives.maintransport'),
        ),
    ]