#!/bin/sh

cd prediction-app-backend && python manage.py flush --no-input
cd prediction-app-backend && python manage.py migrate