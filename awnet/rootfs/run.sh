#!/usr/bin/with-contenv bashio

export PASSKEY_OVERRIDE=$(bashio::config 'passkey_override')

LOG_LEVEL=$(bashio::config 'log_level')
python3 awnet.py $LOG_LEVEL