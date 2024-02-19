#!/usr/bin/env bash
# exit on error
set -o errexit

DJANGO_SETTINGS_MODULE=django_reminders.settings;

pipenv install
pipenv run python manage.py migrate
