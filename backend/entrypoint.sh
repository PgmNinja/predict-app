#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py runserver 0.0.0.0:$PORT

exec "$@"
