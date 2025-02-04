#!/bin/bash

python SustainabilityApp/manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 SustainabilityApp.wsgi:application