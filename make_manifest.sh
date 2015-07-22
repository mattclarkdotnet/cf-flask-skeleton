#!/usr/bin/env bash

SPACE=$1
APP_NAME="skeleton-"`git rev-parse --short HEAD`
TEMPLATE_MANIFEST_FILE="template-manifest-$SPACE.yml"
MANIFEST_FILE="manifest.yml"

echo "Creating manifest $MANIFEST_FILE from template $TEMPLATE_MANIFEST_FILE with APP_NAME=$APP_NAME"
sed -e "s/APP_NAME/$APP_NAME/" $TEMPLATE_MANIFEST_FILE > $MANIFEST_FILE
