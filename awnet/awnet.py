#Adapted for use in HASS ADDON by Dan C Williams: dan.c.williams@gmail.com 20210713

# Python script to decode Ambient Weather data (from WS-2902C and similar)
# and publish to MQTT.
# original author: Austin of austinsnerdythings.com
# publish date: 2021-03-20

# some resources I used include
#https://askubuntu.com/questions/29152/how-do-i-use-python-with-apache2
#https://www.toptal.com/python/pythons-wsgi-server-application-interface
#https://www.emqx.io/blog/how-to-use-mqtt-in-python

from urllib.parse import urlparse, parse_qs
import paho.mqtt.client as mqtt
import time, os

# set MQTT vars
MQTT_BROKER_HOST    = os.getenv('MQTT_BROKER_HOST',"mqtt")
print(MQTT_BROKER_HOST)
MQTT_BROKER_PORT    = int(os.getenv('MQTT_BROKER_PORT',1883))
MQTT_CLIENT_ID      = os.getenv('MQTT_CLIENT_ID',"ambient_weather_decode")
MQTT_USERNAME       = os.getenv('MQTT_USERNAME',"")
MQTT_PASSWORD       = os.getenv('MQTT_PASSWORD',"")

# looking to get resultant topic like weather/ws-2902c/[item]
MQTT_TOPIC_PREFIX   = os.getenv('MQTT_TOPIC_PREFIX',"weather")
MQTT_TOPIC          = os.getenv('MQTT_TOPIC_PREFIX',"station")
COMPILED_MQTT_TOPIC = MQTT_TOPIC_PREFIX + "/" + MQTT_TOPIC

# mostly copied + pasted from https://www.emqx.io/blog/how-to-use-mqtt-in-python and some of my own MQTT scripts
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"connected to MQTT broker at {MQTT_BROKER_HOST}")
    else: 
        print("Failed to connect, return code %d\n", rc)

def on_disconnect(client, userdata, flags, rc):
    print("disconnected from MQTT broker")

# set up mqtt client
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    print("Username and password set.")
client.will_set(MQTT_TOPIC_PREFIX+"/status", payload="Offline", qos=1, retain=True) # set LWT     
client.on_connect = on_connect # on connect callback
client.on_disconnect = on_disconnect # on disconnect callback

# connect to broker
client.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT)
client.loop_start()

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]

    # uncomment for debug. don't need all the success messages.
    if status == 0:
        #print(f"Sent {msg} to topic {topic}")
        pass
    else:
        print(f"Failed to send message to topic {topic}")


def handle_results(result):
    """ result is a dict. full list of variables include:
    stationtype: ['AMBWeatherV4.2.9'], PASSKEY: ['<station_mac_address>'], dateutc: ['2021-03-20 17:12:27'], tempinf: ['71.1'], humidityin: ['36'], baromrelin: ['29.693'],    baromabsin: ['24.549'],    tempf: ['58.8'], battout: ['1'], humidity: ['32'], winddir: ['215'],windspeedmph: ['0.0'],    windgustmph: ['0.0'], maxdailygust: ['3.4'], hourlyrainin: ['0.000'],    eventrainin: ['0.000'],    dailyrainin: ['0.000'],
    weeklyrainin: ['0.000'], monthlyrainin: ['0.000'], totalrainin: ['0.000'],    solarradiation: ['121.36'],
    uv: ['1'],batt_co2: ['1'] """

    # we're just going to publish everything. less coding.
    for key in result:
        # skip first item, which is basically a URL and MQTT doesn't like it. probably resulting from my bad url parsing.
        if 'http://' in key:
            continue

        #print(f"{key}: {result[key]}")
        # resultant topic is weather/ws-2902c/solarradiation
        specific_topic = COMPILED_MQTT_TOPIC + f"/{key}"

        # replace [' and '] with nothing. these come from the url parse
        msg = str(result[key]).replace("""['""", '').replace("""']""", '')
        #print(f"attempting to publish to {specific_topic} with message {msg}")
        publish(client, specific_topic, msg)


def application(environ, start_response):
    # construct a full URL from the request. HTTP_HOST is FQDN, PATH_INFO is everything after
    # the FQDN (i.e. /data/stationtype=AMBWeatherV4.2.9&&tempinf=71.1&humidityin=35)
    url = "http://" + environ["HTTP_HOST"] + environ["PATH_INFO"]

    # unsure why I need to parse twice. probably just need to do it once with variable url.
    parsed = urlparse(url)
    result = parse_qs(parsed.geturl())

    # send to our other function to deal with the results.
    # result is a dict 
    handle_results(result)

    # we need to return a response. HTTP code 200 means everything is OK. other HTTP codes include 404 not found and such.
    start_response('200 OK', [('Content-Type', 'text/plain')])

    # the response doesn't actually need to contain anything
    response_body = ''

    # return the encoded bytes of the response_body. 
    # for python 2 (don't use python 2), the results don't need to be encoded
    return [response_body.encode()]

# this little guy runs a web server if this python file is called directly. if it isn't called directly, it won't run.
# Apache/Python WSGI will run the function 'application()' directly
# in theory, you don't need apache or any webserver. just run it right out of python. would need
# to improve error handling to ensure it run without interruption.
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # probably shouldn't run on port 80 but that's what I specified in the ambient weather console
    httpd = make_server('', 80, application)
    print("Serving on http://localhost:80")

    httpd.serve_forever()