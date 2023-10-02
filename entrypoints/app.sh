#!/bin/bash


while ! nc -z db 5432; do
  sleep 0.1
done

echo "Runserver starting"

python manage.py loaddata budget/fixtures/users.json budget/fixtures/categories.json budget/fixtures/budgets.json budget/fixtures/incomes.json budget/fixtures/expenses.json
python manage.py runserver --insecure 0.0.0.0:8000