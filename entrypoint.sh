#! /bin/sh

# !CHANGE FILE CONFIG IF NEEDED

echo "Start executing workers..."

host=${HOST-127.0.0.1}
workers=${WORKERS-4}
container_type=${CONTAINER_TYPE}

if [ "$container_type" = "DAGSTER_CONTAINER" ]; then
echo "Start executing dagster container..."
gunicorn threatintel.threatintel.wsgi --bind "$host" --workers="$workers" -t 0 --preload --log-file -

elif [ "$container_type" = "ENRICHMENT_CONTAINER" ]; then
echo "Start executing enrichment container..."
python3 manage.py cron_enrichment
python3 manage.py migrate
python3 manage.py collectstatic --no-input

elif [ "$container_type" = "WORKER_CONTAINER" ]; then
echo "Start executing worker container..."
gunicorn threatintel.threatintel.wsgi --bind "$host" --workers="$workers" -t 0 --preload --log-file -

fig
