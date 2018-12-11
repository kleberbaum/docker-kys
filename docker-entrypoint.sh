#!/bin/sh
set -e

#until psql $DATABASE_URL -c '\l'; do
#  >&2 echo "Postgres is unavailable - sleeping"
#  sleep 1
#done

#>&2 echo "Postgres is up - continuing"

# Check if MariaDB is up and accepting connections.
HOSTNAME=$(/venv/bin/python -c "from urllib.parse import urlparse; o = urlparse('$DATABASE_URL'); print(o.hostname);")
until mysqladmin ping --host "$HOSTNAME" --silent; do
    >&2 echo "MariaDB is unavailable - sleeping"
    sleep 1
done
>&2 echo "MariaDB is up - continuing"

>&2 echo "correct ownership of media"
chown -Rv 1000:2000 /code/media/

if [ "$1" = '/venv/bin/uwsgi' ]; then
    /venv/bin/python manage.py migrate --noinput
fi

if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
	/venv/bin/python manage.py load_initial_data
fi

exec "$@"
