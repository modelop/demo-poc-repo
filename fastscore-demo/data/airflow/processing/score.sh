#!/bin/bash

fastscore connect https://dashboard:8000
fastscore -wait fleet
cd /usr/local/airflow/processing

fastscore use engine-5
fastscore engine reset
fastscore model load influx-mux
fastscore stream attach influx-mux-kafka 0
fastscore engine inspect

fastscore use engine-3
fastscore engine reset
fastscore run lr-2 lr-input-file influx-mux-kafka
fastscore engine inspect
