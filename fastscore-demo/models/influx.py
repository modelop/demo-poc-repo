# fastscore.schema.$in: tagged-double
# fastscore.slot.1: unused
# fastscore.module-attached: influxdb

from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep

def begin():
    global influx, FLUSH_DELTA, BATCH_SIZE, BATCH
    FLUSH_DELTA = 0.01
    BATCH_SIZE = 10
    BATCH = []
    influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

def gen_point(name, value, timestamp):
    point = {
        "measurement": name,
        "time": timestamp,
        "fields": {
            "value": value,
            "timestamp": timestamp
        }
    }
    return point

def action(datum):
    global BATCH
    name = datum['name']
    value = datum['value']
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    BATCH.append(gen_point(name, value, timestamp))

    if BATCH_SIZE == len(BATCH):
        influx.write_points(BATCH)
        BATCH = []
        sleep(FLUSH_DELTA)
