#!/bin/bash

CONTAINER_NAME="inmanage-back_db_1"
DB_NAME="inmanage"
DB_USER="postgres"
DB_PASSWORD="samara63"

# Очистка базы данных
echo "Очистка базы данных..."
docker exec -it $CONTAINER_NAME psql -U $DB_USER -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker exec -it $CONTAINER_NAME psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
echo "База данных очищена."

# Выполнение миграций
echo "Выполнение миграций..."
docker exec -it inmanage-back_web_1 python manage.py migrate
echo "Миграции выполнены."

# Создание суперпользователя
echo "Создание суперпользователя..."
docker exec -i inmanage-back_web_1 python manage.py createsuperuser --username admin
echo "Введите пароль для суперпользователя (samara63):"
docker exec -it inmanage-back_web_1 python manage.py changepassword admin
echo "Суперпользователь создан."

echo "Процесс завершен."
