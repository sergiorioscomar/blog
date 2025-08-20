#!/usr/bin/env bash
set -e

echo "Esperando a MySQL (db:3306)..."
until nc -z db 3306; do
  sleep 2
done
echo "MySQL OK"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Lanza Gunicorn (o como módulo, por si PATH)
exec python -m gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 60
