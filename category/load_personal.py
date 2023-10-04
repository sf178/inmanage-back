import json
import psycopg2
from psycopg2.extras import execute_values

# Загрузка JSON файла
with open('D:\inmanage-site\/test_backend\category\categories.json', 'r', encoding='utf-8') as file:
    personal_data = json.load(file)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="inmanage",
    user="postgres",
    password="samara63"
)

cursor = conn.cursor()

# Функция для добавления категории
def insert_personal_category(name):
    cursor.execute("INSERT INTO category_expensepersonalcategory (name) VALUES (%s) RETURNING id;", (name,))
    return cursor.fetchone()[0]


# Обход данных
for personal_category_name in personal_data:
    insert_personal_category(personal_category_name)

def print_data():
    cursor.execute("SELECT id, name FROM category_expensepersonalcategory;")
    personal_categories = cursor.fetchall()
    for category in personal_categories:
        category_name = category[1]
        print(f"Личная Категория: {category_name}")

    print("Данные успешно извлечены и выведены.")

print_data()

conn.commit()
cursor.close()
conn.close()
