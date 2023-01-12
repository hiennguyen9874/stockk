#! /usr/bin/env bash
set -e

# Let the DB start
python /app/app/celery_pre_start.py

# celery worker -A app.worker --loglevel=INFO -Q main-queue -c 1
celery -A app.worker beat --loglevel=INFO
