#!/bin/sh

sleep 20
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files
python manage.py loaddata socialNetworkApp.json #Loads data

# Start Gunicorn
exec gunicorn socialNetwork.wsgi:application \
	 --bind 0.0.0.0:8008 \
	 "$@"
