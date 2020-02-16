import os
import Adafruit_DHT
from influxdb import InfluxDBClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

INFLUX_HOST = os.getenv('INFLUX_HOST', '127.0.0.1')
INFLUX_PORT = os.getenv('INFLUX_PORT', '8086')
INFLUX_USER = os.getenv('INFLUX_USER', '')
INFLUX_PASS = os.getenv('INFLUX_PASS', '')
INFLUX_DATABASE = os.getenv('INFLUX_DATABASE', 'default')
INFLUX_RETENTION_POLICY = os.getenv('INFLUX_RETENTION_POLICY', 'default')
DHT_SENSOR = os.getenv('DHT_SENSOR', '2302')
GPIO_PIN = os.getenv('GPIO_PIN', '4')

#client = InfluxDBClient(host='127.0.0.1', port=8086, username=INFLUX_USER, password=INFLUX_PASS, database='dbname')

try:
    h, t = Adafruit_DHT.read_retry(DHT_SENSOR, GPIO_PIN)
    if h is not None and t is not None:
        points = f"{temperature: t, humidity: h}"
        print (points)

        #https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#influxdb.InfluxDBClient.write_points
        #client.write_points(points, retention_policy=None, protocol=u'line')
except:
    print ("ERROR getting temperature and humidity values")
