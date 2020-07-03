#!/usr/bin/env bash
#######################################
# Entrypoint for Django Docker image.
# Steps down from root user to a gunicorn user
# Globals:
#   APP_DIR
#   DJANGO_DEBUG (optional)
#   DJANGO_DATABASE_URL (optional)
#######################################

set -Eeo pipefail;
if [[ -n "$DJANGO_DEBUG" ]]; then
    set -x;
    echo "Environment:";
    env;
else
    set -u;
fi

wait_for_postgres_ready() {
    #######################################
    # Wait for a postgres database to be available.
    # Arguments:
    #   DJANGO_DATABASE_URL
    #   max_wait (default: 30 seconds)
    #######################################
    local url max_wait n exit_code;
    url="$1";
    max_wait="${2:-30}";
    n=0;
    until [ "$n" -gt "$max_wait" ]; do
        set +e
        python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("""$url""")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
        exit_code=$?;
        set -e;
        if [ "$exit_code" -eq 0 ]; then
            break;
        fi
        if [ "$n" -eq "$max_wait" ]; then
            break;
        fi
        echo "Postgres is unavailable - sleeping" >&2;
        sleep 1;
        n=$((n + 1));
    done
    if [ $exit_code -eq 0 ]; then
        echo "Postgres is up - continuing..." >&2;
    else
        echo "ERROR: Postgres didn't come up!" >&2;
        exit $exit_code;
    fi
}

cd "$APP_DIR";

# Copy nginx config into position
cp -rf config/nginx/* /etc/nginx/conf.d

# Collect Djagno static files.
python -B manage.py collectstatic --noinput;

if [[ "$DJANGO_DATABASE_URL" = "postgresql"* ]]; then
    # If using a PostgreSQL database, wait for it to be available.
    wait_for_postgres_ready "$DJANGO_DATABASE_URL";
fi

# Do database migrations.
python -B manage.py migrate;

if [[ -n "${DJANGO_DEBUG:-}" ]]; then
    # If DJANGO_DEBUG, watch source files for changes and reload if they do.
    # This lets a developer mount their source dir and see changes in real time.
    gunicorn config.wsgi --config "$APP_DIR/config/gunicorn.py" --user nobody --reload "$@";
else
    gunicorn config.wsgi --config "$APP_DIR/config/gunicorn.py" --user nobody --preload "$@";
fi
