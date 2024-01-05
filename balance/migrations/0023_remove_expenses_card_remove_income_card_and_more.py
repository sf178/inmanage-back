from django.db import migrations, models
import django.db.models.deletion

def convert_category(apps, schema_editor):
    Expenses = apps.get_model('balance', 'Expenses')
    for expense in Expenses.objects.all():
        if expense.category:
            # Преобразуйте значение поля 'category' в соответствии с вашей логикой
            # Например, вам может потребоваться выбрать одно значение из массива или выполнить некоторые вычисления
            expense.new_category = int(expense.category[0])  # Пример преобразования
            expense.save()

class Migration(migrations.Migration):

    dependencies = [
        ('category', '0011_personalcategory_subcategory_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('balance', '0022_income_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenses',
            name='card',
        ),
        migrations.RemoveField(
            model_name='income',
            name='card',
        ),
        migrations.AddField(
            model_name='expenses',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='expenses',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='income',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='expenses',
            name='new_category',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.RunPython(convert_category, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='expenses',
            name='category',
        ),
        migrations.RenameField(
            model_name='expenses',
            old_name='new_category',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='expenses',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='category.personalcategory'),
        ),
    ]
