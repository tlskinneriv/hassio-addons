#!/usr/bin/with-contenv bashio

LOG_LEVEL=$(bashio::config 'log_level')
python3 awnet.py $LOG_LEVEL