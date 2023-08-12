import json
from category.models import *
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_backend.settings')
django.setup()


def load_expenses_from_json(json_path):
    with open(json_path, 'r') as file:
        json_data = json.load(file)

    for category_name, subcategories in json_data.items():
        category = ExpensePersonalCategory.objects.create(name=category_name)

        if subcategories:
            for subcategory_name in subcategories.keys():
                subcategory = ExpensePersonalSubcategory.objects.create(name=subcategory_name)
                category.sub_categories.add(subcategory)
        category.save()


# Путь к вашему файлу JSON
json_path = 'categories.json'

load_expenses_from_json(json_path)