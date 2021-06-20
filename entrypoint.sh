#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir -p /code/logs
cd /code

export DJANGO_SETTINGS_MODULE=main_backend.settings

exec gunicorn main_backend.wsgi:application \
    --name main_backend \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level=debug
"$@"
