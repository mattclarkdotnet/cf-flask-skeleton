#!/usr/bin/env bash

python -V 2>&1 | tr '[:upper:]' '[:lower:]' | tr '[:blank:]' '-' > runtime.txt
