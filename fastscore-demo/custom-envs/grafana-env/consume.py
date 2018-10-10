#/usr/bin/os.getenv python3

import potsdb

import json
import requests
import os
from time import sleep

from fastscore.suite import Connect
from fastscore.pneumo import *

MSG_TYPES = []

ENGINE_HOSTNAME = ""

MAX_RECONNECT_COUNT = 100


def init_filters():
    global MSG_TYPES
    global ENGINE_ID
    global MAX_RECONNECT_COUNT
    if os.getenv("MAX_RECONNECT_COUNT") is not None:
        MAX_RECONNECT_COUNT = os.getenv("MAX_RECONNECT_COUNT")
    if os.getenv("ENGINE_ID") is not None:
        ENGINE_ID = os.getenv("ENGINE_ID")
    if os.getenv("ENGINE_HOSTNAME") is not None:
        ENGINE_HOSTNAME = os.getenv("ENGINE_HOSTNAME")
    if os.getenv("HealthMsg") is not None:
        MSG_TYPES += [(HealthMsg, "HealthMsg")]
    if os.getenv("EngineStateMsg") is not None:
        MSG_TYPES += [(EngineStateMsg, "EngineStateMsg")]
    if os.getenv("SensorReportMsg") is not None:
        MSG_TYPES += [(SensorReportMsg, "SensorReportMsg")]
    if os.getenv("ModelErrorMsg") is not None:
        MSG_TYPES += [(ModelErrorMsg, "ModelErrorMsg")]


if __name__ == '__main__':
    if os.getenv("PROXY_PREFIX") is None:
        raise ValueError("PROXY_PREFIX not defined")
    init_filters()
    for i in range(0, MAX_RECONNECT_COUNT):
        try:
            connect = Connect(os.getenv("PROXY_PREFIX"))
            socket = connect.pneumo.socket()
        except:
            sleep(1)
            continue
        break
    for i in range(0, MAX_RECONNECT_COUNT):
        try:
            metrics = potsdb.Client('opentsdb')
        except:
            sleep(1)
            continue
        break
    while(True):
        msg = socket.recv()
	if ENGINE_HOSTNAME != "" and msg.src != ENGINE_HOSTNAME:
            continue
        if reduce(lambda x, y: x or y, map(lambda x: isinstance(msg, x[0]), MSG_TYPES)):
            if isinstance(msg, HealthMsg):
                name = filter(lambda x: x[0] == HealthMsg, MSG_TYPES)[0][1]
                metrics.send(name, msg.health != "ok")
            elif isinstance(msg, EngineStateMsg):
                name = filter(lambda x: x[0] ==
                              EngineStateMsg, MSG_TYPES)[0][1]
                if msg.state == "INIT":
                    metrics.send(name, 0)
                elif msg.state == "RUNNING":
                    metrics.send(name, 1)
                elif msg.state == "FINISHING":
                    metrics.send(name, 2)
                elif msg.state == "FINISHED":
                    metrics.send(name, 3)
            elif isinstance(msg, SensorReportMsg):
                name = filter(lambda x: x[0] ==
                              SensorReportMsg, MSG_TYPES)[0][1]
                metrics.send(name + "." + msg.src + "." + msg.point, msg.data)
