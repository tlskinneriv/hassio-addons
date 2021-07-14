#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

export ENTITY_ID="$(bashio::config 'entity_id')"
export PUBLISH_ALL="$(bashio::config 'publish_all_sensors')"

python3 awnet.py