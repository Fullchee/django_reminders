#!/usr/bin/env bash
# exit on error
set -o errexit

cp sample.env .env
./build.sh
