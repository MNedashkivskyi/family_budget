#!/bin/sh

while ! nc -z django 8000; do
  sleep 0.1
done

echo "Tests starting"

cd /app/
python manage.py test budget/tests/
