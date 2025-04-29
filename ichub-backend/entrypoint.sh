#!/bin/sh
set -e

# In k8s deployments ConfigMaps are mounted as readOnlyRootFilesystem
# so we need to mount the ConfigMap to a tmp folder from which we copy to a writable location
# the code below will copy the ConfigMap content to the symbolinc lynks in /tmp
# that are used by the application
CONFIGMAP_FOLDER="/tmp/config"
CONFIG_FILE="/tmp/configuration.yml"
REFERENCE_FILE="/tmp/configuration.yml.reference"

# Check if the config folder exists
if [ -d "$CONFIGMAP_FOLDER" ]; then
    cp "$CONFIGMAP_FOLDER/configuration.yml" tmp/configuration.yml.reference
    cp "$CONFIGMAP_FOLDER/logging.yml" tmp/logging.yml
fi

# Render config using envsubst
if envsubst < "$REFERENCE_FILE" > "$CONFIG_FILE"; then
  echo "Configuration rendered successfully."
else
  echo "ERROR: Failed to render configuration."
  exit 1
fi

python3 -m main --host 0.0.0.0 --port 8000