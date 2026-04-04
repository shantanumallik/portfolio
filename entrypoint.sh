#!/bin/sh
set -e

echo "Running deploy seed..."
python deploy_seed.py

echo "Starting gunicorn..."
exec gunicorn run:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120
