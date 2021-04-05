import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

INFLUX_HOST = os.getenv('INFLUX_HOST', '127.0.0.1')
INFLUX_PORT = os.getenv('INFLUX_PORT', '8086')
INFLUX_USER = os.getenv('INFLUX_USER', '')
INFLUX_PASS = os.getenv('INFLUX_PASS', '')
INFLUX_DATABASE = os.getenv('INFLUX_DATABASE', 'default')
INFLUX_RETENTION_POLICY = os.getenv('INFLUX_RETENTION_POLICY', 'default')
INFLUX_SSL = os.getenv('INFLUX_SSL', False)
LOGFILE='/var/log/influx_temps_debug.log'