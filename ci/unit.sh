#!/usr/bin/env bash

cd cf-flask-skeleton
pip install -r requirements.txt
nosetests test/unit/test_skeleton.py