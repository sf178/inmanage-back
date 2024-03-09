# Generated by Django 4.1.7 on 2024-03-07 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('passives', '0042_mainborrows_passives_borrows'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalloans',
            name='content_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='historicalloans',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='loans',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='loans',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]