#!/bin/sh
set -e

#until psql $DATABASE_URL -c '\l'; do
#  >&2 echo "Postgres is unavailable - sleeping"
#  sleep 1
#done

#>&2 echo "Postgres is up - continuing"

>&2 echo "correct ownership of media"
chown -Rv 1000:2000 /code/media/

if [ "$1" = '/venv/bin/uwsgi' ]; then
    /venv/bin/python manage.py migrate --noinput
fi

if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
	/venv/bin/python manage.py load_initial_data
fi

exec "$@"
