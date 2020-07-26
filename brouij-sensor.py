#!/usr/bin/python3
# coding: utf8

import json
import os
import signal
import statsd
import time

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

c = statsd.StatsClient(
        conf["graphite_server"],
        8125)


sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

while running:
    temp = sensor.readTempC()
    print ('Thermocouple Temperature: {0:0.3F}°'.format (temp))
    c.gauge('temperature.%s.mash' % ( conf["current_beer"],), temp)
    time.sleep(5.0)
    
c.gauge('temperature.%s.mash' % ( conf["current_beer"],), None)
