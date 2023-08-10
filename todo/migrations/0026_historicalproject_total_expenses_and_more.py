# Generated by Django 4.1.7 on 2023-08-10 00:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0025_historicalproject_expenses_is_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproject',
            name='total_expenses',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalproject',
            name='total_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planner',
            name='total_expenses',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='planner',
            name='total_income',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='planner',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='project',
            name='total_expenses',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='total_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planner',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='planners', to='todo.project'),
        ),
        migrations.AlterField(
            model_name='planner',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='todo.todotask'),
        ),
    ]
