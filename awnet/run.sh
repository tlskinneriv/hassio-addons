#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

export MQTT_BROKER_HOST="$(bashio::config 'mqtt_host')"
export MQTT_BROKER_PORT="$(bashio::config 'mqtt_port')"
export MQTT_USERNAME="$(bashio::config 'mqtt_user')"
export MQTT_PASSWORD="$(bashio::config 'mqtt_password')"
export MQTT_TOPIC_PREFIX="$(bashio::config 'mqtt_topic_prefix')"
export MQTT_TOPIC="$(bashio::config 'mqtt_topic')"

python3 awnet.py