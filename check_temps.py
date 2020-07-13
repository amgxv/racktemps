#!/usr/bin/python3

import Adafruit_DHT
from influxdb import InfluxDBClient
import statistics
import logging
from envs import *


def push():
    temp = []
    hum = []

    logging.basicConfig(level=logging.DEBUG, filename=LOGFILE, filemode='w')

    try:
        if INFLUX_SSL == "True":
            client = InfluxDBClient(
                host=INFLUX_HOST,
                ssl=True,
                verify_ssl=False,
                port=INFLUX_PORT,
                username=INFLUX_USER,
                password=INFLUX_PASS,
                database=INFLUX_DATABASE
            )
        else:
            client = InfluxDBClient(
                host=INFLUX_HOST,
                port=INFLUX_PORT,
                username=INFLUX_USER,
                password=INFLUX_PASS,
                database=INFLUX_DATABASE
            )

        for i in range(5):
            logging.debug('Starting read {}'.format(i))
            h, t = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, GPIO_PIN)
            if h is not None and t is not None:
                logging.debug('Temperature {}'.format(temp))
                temp.append(t)
                logging.debug('Humidity {}'.format(hum))
                hum.append(h)

        temp = statistics.median(sorted(temp))
        logging.debug('Temperature median : {}'.format(temp))
        hum = statistics.median(sorted(hum))
        logging.debug('Humidity median : {}'.format(hum))

        points = [
           {
               "measurement": "temperature",
               "fields": {
                   "value": temp
               }
           },
           {
               "measurement": "humidity",
               "fields": {
                   "value": hum
               }
           }
        ]

        # https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#influxdb.InfluxDBClient.write_points
        logging.debug('Writing points to InfluxDB {}/{}'.format(
            INFLUX_HOST,
            INFLUX_DATABASE
        ))
        client.write_points(
            points,
            retention_policy=INFLUX_RETENTION_POLICY,
            protocol=u'json'
        )
    except Exception as e:
        print("ERROR: ", e)

if __name__ == "__main__":
    push()
