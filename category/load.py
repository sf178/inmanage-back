import json
import psycopg2
from psycopg2.extras import execute_values

# Загрузка JSON файла
with open('D:\inmanage-site\/test_backend\category\categories.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inmanage-test",
    user="postgres",
    password="samara63"
)

cursor = conn.cursor()

# Функция для добавления категории
def insert_category(name):
    cursor.execute("INSERT INTO category_expensepersonalcategory (name) VALUES (%s) RETURNING id;", (name,))
    return cursor.fetchone()[0]

# Функция для добавления подкатегории
def insert_subcategory(name, category_id):
    cursor.execute("INSERT INTO category_expensepersonalsubcategory (name, category_id) VALUES (%s, %s) RETURNING id;", (name, category_id))
    return cursor.fetchone()[0]

# Обход данных
for category_name, subcategories in data.items():
    category_id = insert_category(category_name)
    if subcategories is not None:
        for subcategory_name in subcategories.keys():
            subcategory_id = insert_subcategory(subcategory_name, category_id)
            cursor.execute("INSERT INTO category_expensepersonalcategory_sub_categories (expensepersonalcategory_id, expensepersonalsubcategory_id) VALUES (%s, %s);", (category_id, subcategory_id))

def print_data():
    cursor.execute("SELECT id, name FROM category_expensepersonalcategory;")
    categories = cursor.fetchall()
    for category in categories:
        category_id, category_name = category
        print(f"Категория: {category_name}")

        cursor.execute("SELECT name FROM category_expensepersonalsubcategory WHERE category_id = %s;", (category_id,))
        subcategories = cursor.fetchall()
        for subcategory in subcategories:
            subcategory_name = subcategory[0]
            print(f"  Подкатегория: {subcategory_name}")

    print("Данные успешно извлечены и выведены.")

print_data()

conn.commit()
cursor.close()
conn.close()
