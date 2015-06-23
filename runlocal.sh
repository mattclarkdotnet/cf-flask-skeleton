#!/usr/bin/env sh

gunicorn -w $GUNICORN_WORKERS -b $LOCAL_IP:$LOCAL_PORT skeleton.server:app
