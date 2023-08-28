# Используйте официальный образ Python 3.10 в качестве базового
FROM python:3.10-slim-buster

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=main.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app

# Экспозируем порт, на котором работает Gunicorn
EXPOSE 8000

# Запускаем команды для создания базы данных, администратора и тестов
CMD ["bash", "-c", "if [ $CREATE_DB = true ]; then python create_words_db.py && python create_admin.py; fi && gunicorn -w 4 -b 0.0.0.0:8000 main:app --workers 1 --threads 2"]

