#!/usr/bin/env bash
# exit on error
set -o errexit

git pull

pip install -r requirements.txt

python manage.py collectstatic --no-input

sudo systemctl restart golf-gunicorn.service
