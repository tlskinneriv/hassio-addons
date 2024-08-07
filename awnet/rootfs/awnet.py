# Adapted for use in Home Assistant by Dan C Williams, tlskinneriv

# https://austinsnerdythings.com/2021/03/20/handling-data-from-ambient-weather-ws-2902c-to-mqtt/?unapproved=64&moderation-hash=2c93b4c769f98120c9adae6be6ca2f18#comment-64
# Python script to decode Ambient Weather data (from WS-2902C and similar)
# and publish to MQTT.
# original author: Austin of austinsnerdythings.com
# publish date: 2021-03-20

# In the event this script is to be used outside of this container configuration, the following
# environment variables must be set for proper operation:
#
# HA_API_BASE_URL: The base URL to your HA instance's API; e.g. http://homeassistant.local:8123/api/
# HA_API_AUTH_TOKEN: A long-lived access token for HA. Create one under user profile -> security.
#
# Optional variables:
#
# HTTP_LISTEN_HOST: Default: "" (all IP addresses); the host that this script will listen on for updates from the AWNET device
# HTTP_LISTEN_PORT: Default: 7080; The port that this script should listen on for updates from the AWNET device
# HA_API_VALIDATE_CERTIFICATE: Default: True; if set to True, verifies the SSL certificate on HTTPS requests
# LOG_LEVEL: Default: WARNING; log level setting; one of: DEBUG, INFO, WARNING, ERROR, CRITICAL
# PASSKEY_OVERRIDE: Default: ""; In the event that the PASSKEY value for the device is not a MAC address, use this field to
# statically set it to your devices MAC address.

from urllib.parse import parse_qs, urljoin
from wsgiref.headers import Headers
from wsgiref.simple_server import WSGIRequestHandler
import re
import json
import requests
import os
import logging
import sys

ATTR_PASSKEY = 'PASSKEY'

_LOGGER = logging.getLogger(__name__)

# set vars
PASSKEY_OVERRIDE = os.environ.get("PASSKEY_OVERRIDE", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
HTTP_LISTEN_HOST = os.getenv("HTTP_LISTEN_HOST", "")
HTTP_LISTEN_PORT = int(os.getenv("HTTP_LISTEN_PORT", "7080"))
HA_API_AUTH_TOKEN = os.getenv("HA_API_AUTH_TOKEN", "test")
HA_API_BASE_URL = os.getenv("HA_API_BASE_URL", "http://supervisor/core/api/")
HA_API_VALIDATE_CERTIFICATE = os.getenv("HA_API_VALIDATE_CERTIFICATE", "True").lower() == 'true'

def get_headers(environ):
    """
    Handles getting the headers from the environment, Content-Type is the special one
    """
    headers = Headers([])
    for header, value in environ.items():
        if header.startswith("HTTP_"):
            headers[header[5:].replace('_','-')] = value
    if 'CONTENT_TYPE' in environ:
        headers['CONTENT-TYPE'] = environ['CONTENT_TYPE']
    return headers


def publish(payload):
    payload_json = json.dumps(payload)

    head = {
        "Authorization": "Bearer " + HA_API_AUTH_TOKEN,
        "content-type": "application/json",
    }
    good_responses = [200, 201]

    url = urljoin(HA_API_BASE_URL, "services/awnet_local/update")

    response = requests.post(url, data=payload_json, headers=head, verify=HA_API_VALIDATE_CERTIFICATE)

    if response.status_code in good_responses:
        _LOGGER.info(f"Sent {payload_json}")
    else:
        _LOGGER.error(f"Failed to send data to Home Assistant. HTTP error code: {response.status_code}.")
        _LOGGER.info(f"Failed payload: {payload_json} to {url} with headers {head}; {response.content}")
        if response.status_code == 400:
            _LOGGER.warning("'Ambient Weather Station - Local' may not be set up. Please install it from HACS and set it up with your device's MAC address.")
        elif response.status_code == 502:
            _LOGGER.warning("Home Assistant may not be available to receive requests.")
        else:
            _LOGGER.warning("An unknown error occurred.")


def handle_results(result):
    """result is a dict. full list of variables include:
    stationtype: ['AMBWeatherV4.2.9'], PASSKEY: ['<station_mac_address>'], dateutc: ['2021-03-20 17:12:27'], tempinf: ['71.1'], humidityin: ['36'], baromrelin: ['29.693'],    baromabsin: ['24.549'],    tempf: ['58.8'], battout: ['1'], humidity: ['32'], winddir: ['215'],windspeedmph: ['0.0'],    windgustmph: ['0.0'], maxdailygust: ['3.4'], hourlyrainin: ['0.000'],    eventrainin: ['0.000'],    dailyrainin: ['0.000'],
    weeklyrainin: ['0.000'], monthlyrainin: ['0.000'], totalrainin: ['0.000'],    solarradiation: ['121.36'],
    uv: ['1'],batt_co2: ['1']"""
    # This changes the resulting key values from lists to single values
    for key in result:
        if len(result[key]) == 1:
            result[key] = result[key][0]
        else:
            _LOGGER.error('Unexpected list size for key %s', key)
    m = re.search(pattern=r'(?:[a-f0-9]{2}[\.\-:]?){5}[a-f0-9]{2}', string=PASSKEY_OVERRIDE, flags=re.IGNORECASE)
    if m is not None:
        _LOGGER.debug('%s override: %s', ATTR_PASSKEY, m[0])
        result[ATTR_PASSKEY] = m[0]
    publish(result)


def application(environ, start_response):
    # the FQDN (i.e. /data?stationtype=AMBWeatherV4.2.9&&tempinf=71.1&humidityin=35)
    # adapted the code to reflect comment from original blog post.
    _LOGGER.debug("Environ is: %s", environ)
    headers = get_headers(environ)
    _LOGGER.debug("Headers: \n\n%s", headers)
    result = parse_qs(environ["QUERY_STRING"])
    _LOGGER.debug("Full Data: %s", result)
    # send to our other function to deal with the results.
    # result is a dict
    if len(result) == 0:
        start_response("400 Bad Request", [("Content-Type", "text/plain")])
        response_body = "Missing query string"
        _LOGGER.debug("Bad Request: %s", response_body)
        _LOGGER.error("Query string could not be detected in the request. Is the query string character '?' in the path?")
    else:
        handle_results(result)
        # we need to return a response. HTTP code 200 means everything is OK. other HTTP codes include 404 not found and such.
        start_response("200 OK", [("Content-Type", "text/plain")])
        # the response doesn't actually need to contain anything
        response_body = ""
        _LOGGER.debug("Valid Request")
    # return the encoded bytes of the response_body.
    # for python 2 (don't use python 2), the results don't need to be encoded
    return [response_body.encode()]


# this little guy runs a web server if this python file is called directly. if it isn't called directly, it won't run.
# Apache/Python WSGI will run the function 'application()' directly
# in theory, you don't need apache or any web server. just run it right out of python. would need
# to improve error handling to ensure it run without interruption.

class AWNETWSGIRequestHandler(WSGIRequestHandler):
    def parse_request(self):
        """
        Adds in logic to handle the poorly formed (non-compliant) request strings that some Ambient Weather devices send.
        """
        requestline = str(self.raw_requestline, 'iso-8859-1')
        requestline = requestline.rstrip('\r\n')
        _LOGGER.debug("original requestline: %s", requestline)
        extra_lines_read = 0
        while re.search(pattern=r'\s+HTTP/\d+\.\d+$', string=requestline, flags=re.IGNORECASE) is None:
            if extra_lines_read == 3:
                _LOGGER.warning("3 extra lines read to detect querystring, but still not detected properly. Aborting extra line reads.")
                break
            raw_extraline = self.rfile.readline(65537)
            if len(raw_extraline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            extraline = str(raw_extraline, 'iso-8859-1')
            extraline = extraline.rstrip('\r\n')
            _LOGGER.debug("extraline: %s", extraline)
            requestline += extraline
            extra_lines_read += 1
        if extra_lines_read > 0:
            new_raw_requestline = requestline.encode('iso-8859-1')
            if len(new_raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            self.raw_requestline = new_raw_requestline
            _LOGGER.debug("new raw_requestline: %s", self.raw_requestline)
        return super().parse_request()

    # Use the built-in log handler rather than outputting to stderr
    def log_message(self, format, *args):
        _LOGGER.info(format, *args)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    logging.basicConfig(stream = sys.stdout,
                    format = '[%(asctime)s] [%(levelname)-8s] %(message)s (%(filename)s:%(lineno)d)',
                    level = LOG_LEVEL)

    # log variable values for DEBUG
    _LOGGER.info("LOG_LEVEL: %s", LOG_LEVEL)
    _LOGGER.info("HTTP_LISTEN_HOST: %s", HTTP_LISTEN_HOST)
    _LOGGER.info("HTTP_LISTEN_PORT: %s", HTTP_LISTEN_PORT)
    _LOGGER.info("HA_API_AUTH_TOKEN: %s", HA_API_AUTH_TOKEN)
    _LOGGER.info("HA_API_BASE_URL: %s", HA_API_BASE_URL)
    _LOGGER.info("HA_API_VALIDATE_CERTIFICATE: %s", HA_API_VALIDATE_CERTIFICATE)

    # probably shouldn't run on port 80 but that's what I specified in the ambient weather console
    httpd = make_server(HTTP_LISTEN_HOST, HTTP_LISTEN_PORT, application, handler_class=AWNETWSGIRequestHandler)
    _LOGGER.info(f"Serving on http://{HTTP_LISTEN_HOST}:{HTTP_LISTEN_PORT}")

    httpd.serve_forever()
