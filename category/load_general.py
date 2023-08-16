import json
import psycopg2
from psycopg2.extras import execute_values


def insert_general_category(name):
    cursor.execute("INSERT INTO category_expensegeneralcategory (name) VALUES (%s) RETURNING id;", (name,))
    return cursor.fetchone()[0]

# Добавление подкатегории
def insert_general_subcategory(name, general_category_id):
    cursor.execute("INSERT INTO category_expensegeneralsubcategory (name, general_category_id) VALUES (%s, %s) RETURNING id;", (name, general_category_id))
    return cursor.fetchone()[0]

# Добавление подвложенной категории
def insert_general_nested_subcategory(name, sub_category_id):
    cursor.execute("INSERT INTO category_expensegeneralnestedsubcategory (name, sub_category_id) VALUES (%s, %s) RETURNING id;", (name, sub_category_id))
    return cursor.fetchone()[0]

def link_subcategory_to_nested_subcategory(subcategory_id, nested_subcategory_id):
    cursor.execute(
        "INSERT INTO category_expensegeneralsubcategory_nested_subcategories (expensegeneralsubcategory_id, expensegeneralnestedsubcategory_id) VALUES (%s, %s);",
        (subcategory_id, nested_subcategory_id))

def link_category_to_subcategory(category_id, subcategory_id):
    cursor.execute(
        "INSERT INTO category_expensegeneralcategory_subcategories (expensegeneralcategory_id, expensegeneralsubcategory_id) VALUES (%s, %s);",
        (category_id, subcategory_id))


# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inmanage-test",
    user="postgres",
    password="samara63"
)

cursor = conn.cursor()

# Загрузка и обработка второго JSON файла (предположим, что он называется 'categories2.json')
with open('D:\inmanage-site\/test_backend\category\categories2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for general_category_name, subcategories in data.items():
    general_category_id = insert_general_category(general_category_name)
    for subcategory_name, nested_subcategories in subcategories.items():
        if nested_subcategories is None:
            subcategory_id = insert_general_subcategory(subcategory_name, general_category_id)
            link_category_to_subcategory(general_category_id, subcategory_id)
        else:
            subcategory_id = insert_general_subcategory(subcategory_name, general_category_id)
            link_category_to_subcategory(general_category_id, subcategory_id)
            for nested_subcategory_name in nested_subcategories.keys():
                nested_subcategory_id = insert_general_nested_subcategory(nested_subcategory_name, subcategory_id)
                link_subcategory_to_nested_subcategory(subcategory_id, nested_subcategory_id)


def print_data():
    cursor.execute("SELECT id, name FROM category_expensegeneralcategory;")
    general_categories = cursor.fetchall()
    for category in general_categories:
        category_id, category_name = category
        print(f"Категория: {category_name}")

        cursor.execute("SELECT name FROM category_expensegeneralsubcategory WHERE general_category_id = %s;",
                       (category_id,))
        subcategories = cursor.fetchall()
        for subcategory in subcategories:
            subcategory_name = subcategory[0]
            print(f"  Подкатегория: {subcategory_name}")

    print("Данные успешно извлечены и выведены.")


print_data()

conn.commit()
cursor.close()
conn.close()
