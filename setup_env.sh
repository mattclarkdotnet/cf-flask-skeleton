#!/usr/bin/env bash

mkvirtualenv --no-site-packages --python=`which python3` cf-flask-skeleton
python -V 2>&1 | tr '[:upper:]' '[:lower:]' | tr '[:blank:]' '-' > runtime.txt
pip install -r requirements.txt
