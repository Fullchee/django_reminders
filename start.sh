#!/usr/bin/env bash
# exit on error
set -o errexit

PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=django_reminders.settings;
pipenv run python manage.py runserver
