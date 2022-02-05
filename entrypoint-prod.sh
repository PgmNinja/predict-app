#!/bin/sh

python prediction-app-backend/manage.py makemigrations --no-input
python prediction-app-backend/manage.py migrate --no-input


