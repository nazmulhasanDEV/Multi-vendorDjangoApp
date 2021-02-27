release: python manage.py migrate --noinput
web: daphne multi_vendor.asgi:application --port $PORT --bind 0.0.0.0
