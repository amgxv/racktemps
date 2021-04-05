#!/usr/bin/python3

from influxdb import InfluxDBClient
import statistics
import logging
from envs import *
from envirophat import weather
from subprocess import PIPE, Popen

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def push():
    temp = []
    hum = []

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        filename=LOGFILE,
        format=log_format,
        filemode='a')
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

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
            cpu_temp_c = get_cpu_temperature()
            temp_c = weather.temperature()
            temp_c_cal = temp_c - ((cpu_temp_c-temp_c)/1.3)
            if temp_c_cal is not None:
                logging.debug('Temperature {}'.format(temp_c_cal))
                temp.append(temp_c_cal)

        logging.debug('Temperature Values : {}'.format(temp))
        temp = statistics.median(sorted(temp))
        logging.debug('Temperature Median : {}'.format(temp))

        points = [
           {
               "measurement": "temperature",
               "fields": {
                   "value": temp
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
