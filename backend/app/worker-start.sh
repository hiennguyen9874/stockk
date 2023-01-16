#! /usr/bin/env bash
set -e

# Let the DB start
python /app/app/celery_pre_start.py

# celery worker -A app.worker -l info -Q main-queue -c 1
celery -A app.worker worker -l info --concurrency ${CELERY_CONCURRENCY}
