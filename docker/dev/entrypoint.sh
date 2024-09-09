#!/bin/sh

python manage.py collectstatic --noinput

python manage.py migrate

daphne -b 0.0.0.0 -p 7777 apps.config.asgi:application