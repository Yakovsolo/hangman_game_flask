FROM python:3.10-slim-buster

ENV FLASK_APP=main.py
ENV CREATE_DB=true  

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]