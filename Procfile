release: python manage.py collectstatic --noinput
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput

web: gunicorn hotel_app.wsgi --log-file -
