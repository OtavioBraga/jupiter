#!/bin/bash
set -e
cmd="$@"

export REDIS_URL=redis://redis:6379
export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

if [[ ${DJANGO_SETTINGS_MODULE} == "config.production" ]]; then
    echo "# PRODUCTION ENV"
    echo "# Execute collectstatic..."
    python /app/manage.py collectstatic --noinput
    echo "# Execute gunicorn"
fi

exec $cmd
