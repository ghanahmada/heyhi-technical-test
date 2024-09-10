#!/bin/bash

# set environment variable for ColBERT extension verbosity
export COLBERT_LOAD_TORCH_EXTENSION_VERBOSE=True

# collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

# apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# start server
echo "Starting server"
gunicorn main.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 240