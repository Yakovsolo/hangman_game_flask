#!/bin/bash

export FLASK_ENV="testing"
python create_db.py
python -m unittest discover -v

export FLASK_ENV="default"

if [ "$CREATE_DB" = "true" ]; then
  while ! nc -z hangman-database 5432; do
    sleep 1
  done

  if [ ! -f /app/db_created ]; then
    python create_words_db.py
    python create_admin.py
    touch /app/db_created  
  fi
fi



exec gunicorn -w 4 -b 0.0.0.0:8000 main:app --workers 1 --threads 2
