release: python manage.py collectstatic --noinput
web: gunicorn bodega.wsgi:application --bind 0.0.0.0:$PORT
