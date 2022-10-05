web: python manage.py runserver 0.0.0.0:\$PORT
web: gunicorn hotel_app.wsgi --log-file -
release: python manage.py makemigrations --noinput
release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput
