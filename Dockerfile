# Используйте официальный образ Python 3.8
FROM python:3.8

# Устанавливает рабочий каталог в /app
WORKDIR /app

# Устанавливает переменные окружения
ENV PYTHONUNBUFFERED 1

# Копирует файлы проекта в контейнер
COPY . /app

# Устанавливает зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Запускает Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "yourproject.wsgi:application"]
