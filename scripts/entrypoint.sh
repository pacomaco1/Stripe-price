#!/bin/bash

while ! nc -z -w 1 $POSTGRES_HOST ${POSTGRES_PORT:-POSTGRES_PORT}; do
  sleep 1
done

sleep 5


python manage.py migrate

python manage.py runserver 0.0.0.0:8000 --noreload
