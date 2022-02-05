#!/bin/sh

cd prediction-app-backend && python manage.py makemigrations --no-input
cd prediction-app-backend && python manage.py migrate --no-input

