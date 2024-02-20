#!/usr/bin/env bash
# exit on error
set -o errexit

export DJANGO_SETTINGS_MODULE=django_reminders.settings;

poetry install
poetry run python manage.py migrate
