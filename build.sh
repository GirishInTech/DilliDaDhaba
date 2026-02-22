#!/usr/bin/env bash
# build.sh — Render build script
# Render runs this once before starting the gunicorn process.
# Every step must succeed (set -o errexit) or the deploy fails fast.

set -o errexit   # exit immediately on any error

echo "==> Installing Python dependencies"
pip install -r requirements.txt

echo "==> Collecting static files"
python manage.py collectstatic --no-input

echo "==> Running database migrations"
python manage.py migrate --no-input

echo "==> Seeding menu data"
# seed_menu wipes and re-inserts on every deploy so the menu
# is always in sync with the source dataset.
python manage.py seed_menu

echo "==> Build complete"
