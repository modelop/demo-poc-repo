#!/bin/bash
fastscore use engine-1
fastscore engine reset
fastscore run neural_net.py neural_net-in neural_net-out_kafka
fastscore use engine-3
fastscore engine reset
fastscore run neural_net.R neural_net-in neural_net-out_kafka
fastscore use engine-4
fastscore engine reset
fastscore run neural_net.ppfa neural_net-in neural_net-out_kafka
python3 ./kafka_1.py
