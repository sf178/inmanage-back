# Generated by Django 4.1.7 on 2023-10-04 19:26

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_remove_customuser_username_customuser_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryCustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('temp_token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='about',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='caption',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.TextField(null=True),
        ),
    ]