#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
python <<'PY'
import os
import time

import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", "5432")
user = os.environ.get("POSTGRES_USER", "task_manager")
password = os.environ.get("POSTGRES_PASSWORD", "task_manager")
dbname = os.environ.get("POSTGRES_DB", "task_manager")

for attempt in range(60):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
        )
        conn.close()
        print("PostgreSQL is ready.")
        break
    except psycopg2.OperationalError:
        time.sleep(1)
else:
    raise SystemExit("PostgreSQL is unavailable")
PY

python manage.py migrate --noinput

if [ "${RUN_COLLECTSTATIC:-0}" = "1" ]; then
  python manage.py collectstatic --noinput
fi

if [ "${SEED_DEMO:-0}" = "1" ]; then
  python manage.py seed_demo
fi

exec "$@"
