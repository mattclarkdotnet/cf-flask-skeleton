#!/usr/bin/env bash

PY3=`which python3`
PY2=`which python2`
if [[ $PY3 != '' ]]; then
    PY=$PY3
else
    PY=$PY2
fi
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --no-site-packages --python=$PY cf-flask-skeleton
pip install -r requirements.txt
