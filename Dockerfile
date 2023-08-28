FROM python:3.10-slim-buster

ENV FLASK_APP=main.py

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["bash", "-c", "if [ $CREATE_DB = true ]; then python create_words_db.py && python create_admin.py; fi && gunicorn -w 4 -b 0.0.0.0:8000 main:app --workers 1 --threads 2"]

