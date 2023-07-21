# Generated by Django 4.1.6 on 2023-05-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_todoitem_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todotask',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='todotask',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='todo.todoitem'),
        ),
    ]
