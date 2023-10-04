import json
import psycopg2
from psycopg2.extras import execute_values


def insert_general_category(name):
    cursor.execute("INSERT INTO category_expensegeneralcategory (name) VALUES (%s) RETURNING id;", (name,))
    return cursor.fetchone()[0]


# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inmanage",
    user="postgres",
    password="samara63"
)

cursor = conn.cursor()

# Загрузка и обработка второго JSON файла (предположим, что он называется 'categories2.json')
with open('D:\inmanage-site\/test_backend\category\categories2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for general_category_name, subcategories in data.items():
    general_category_id = insert_general_category(general_category_name)



def print_data():
    cursor.execute("SELECT id, name FROM category_expensegeneralcategory;")
    general_categories = cursor.fetchall()
    for category in general_categories:
        category_id, category_name = category
        print(f"Категория: {category_name}")


    print("Данные успешно извлечены и выведены.")


print_data()

conn.commit()
cursor.close()
conn.close()
