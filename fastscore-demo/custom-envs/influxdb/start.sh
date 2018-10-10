#!/usr/bin/env sh

influxd &
sleep 5
influx < /etc/fastscore.dump
kill $!
influxd
