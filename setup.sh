#!/usr/bin/env bash
# exit on error
set -o errexit

./build.sh
git update-index --assume-unchanged .env
poetry run pre-commit install
