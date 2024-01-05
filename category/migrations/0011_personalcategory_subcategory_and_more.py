# Generated by Django 4.1.7 on 2024-01-05 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0010_category_assetcategory_liabilitycategory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalCategory',
            fields=[
                ('category_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='category.category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('category.category',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='expensegeneralcategory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='expensesubcategory',
            name='general_category',
        ),
        migrations.RemoveField(
            model_name='liabilitycategory',
            name='category_ptr',
        ),
        migrations.RemoveField(
            model_name='personalexpensecategory',
            name='category_ptr',
        ),
        migrations.RemoveField(
            model_name='personalexpensecategory',
            name='user',
        ),
        migrations.AlterField(
            model_name='category',
            name='icon_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AssetCategory',
        ),
        migrations.DeleteModel(
            name='ExpenseGeneralCategory',
        ),
        migrations.DeleteModel(
            name='ExpenseSubCategory',
        ),
        migrations.DeleteModel(
            name='LiabilityCategory',
        ),
        migrations.DeleteModel(
            name='PersonalExpenseCategory',
        ),
        migrations.AddField(
            model_name='category',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='category.subcategory'),
        ),
    ]
