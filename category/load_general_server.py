import json
import psycopg2
from psycopg2.extras import execute_values


def insert_general_category(name, subcategories):
    cursor.execute("INSERT INTO category_expensegeneralcategory (name) VALUES (%s) RETURNING id;", (name,))
    general_category_id = cursor.fetchone()[0]

    # Добавление подкатегорий для каждой основной категории
    for subcategory_name in subcategories:
        cursor.execute("INSERT INTO category_expensesubcategory (name, general_category_id) VALUES (%s, %s);",
                       (subcategory_name, general_category_id))

    return general_category_id

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inmanage",
    user="postgres",
    password="samara63",
    host="inmanage-back_db_1"
)

cursor = conn.cursor()

# Загрузка и обработка второго JSON файла (предположим, что он называется 'categories2.json')
with open('./category/categories2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for general_category_name, subcategories in data.items():
    insert_general_category(general_category_name, subcategories)

def print_data():
    cursor.execute("SELECT id, name FROM category_expensegeneralcategory;")
    general_categories = cursor.fetchall()
    for category in general_categories:
        category_id, category_name = category
        print(f"Категория: {category_name}")

        # Извлекаем и выводим подкатегории для каждой основной категории
        cursor.execute("SELECT name FROM category_expensesubcategory WHERE general_category_id = %s;", (category_id,))
        subcategories = cursor.fetchall()
        for subcategory_name in subcategories:
            print(f"  Подкатегория: {subcategory_name[0]}")

    print("Данные успешно извлечены и выведены.")

print_data()

conn.commit()
cursor.close()
conn.close()
