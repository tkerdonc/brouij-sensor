#!/usr/bin/python3
# coding: utf8

import json
import os
import signal
import time
from datetime import datetime

from influxdb import InfluxDBClient
import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675


SPI_PORT   = 0
SPI_DEVICE = 0

running = True

def handler(signum, frame):
    global running
    running = False

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGINT, handler)

# This open() may hang indefinitely


conf_path = os.environ.get("SENSOR_CONF") or "./conf.json"

conf = json.load(open(conf_path))


client = InfluxDBClient(host=conf['server_host'],
                        database="brewing",
                        use_udp=True,
                        udp_port=conf['server_port'])

sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

while running:
    temp = sensor.readTempC()
    json_body = {
        "tags": {
            "beer": conf["current_beer"],
            "phase": conf["current_phase"],
        },
        "points": [{
            "measurement": "temperature",
            "fields": {
                "value": temp,
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }]
    }

    client.send_packet(json_body)
    time.sleep(5.0)
