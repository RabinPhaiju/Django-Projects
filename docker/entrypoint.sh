#!/bin/bash

set -e

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

: ${WAIT_TIMEOUT:=60}
: ${DB_HOST:=db}
: ${DB_PORT:=5432}

case "$1" in
  manage)
    shift
    exec /home/wait-for-it.sh $DB_HOST:$DB_PORT -s -t $WAIT_TIMEOUT -- python manage.py "$@"
    ;;
  run)
    shift
    exec /home/wait-for-it.sh $DB_HOST:$DB_PORT -s -t $WAIT_TIMEOUT -- python manage.py shell < "$1"
    ;;
  *)
    exec "$@"
esac

exit 0
