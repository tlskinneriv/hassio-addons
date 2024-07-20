#!/usr/bin/with-contenv bashio

export PASSKEY_OVERRIDE=${PASSKEY_OVEFRRRIDE:-$(bashio::config 'passkey_override')}
export LOG_LEVEL=${LOG_LEVEL:-$(bashio::config 'log_level')}
export HA_API_AUTH_TOKEN=${HA_API_AUTH_TOKEN:-$SUPERVISOR_TOKEN}

python3 awnet.py