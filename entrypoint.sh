#!/bin/env
echo "Running migrations..."
python manage.py migrate

echo "Create superuser..."
python manage.py create_su

echo "Collect static files..."
python manage.py collectstatic --noinput


echo "Starting gunicorn..."
gunicorn --bind 0.0.0.0:9000 --workers 3 config.wsgi:application 0
exec "$@"