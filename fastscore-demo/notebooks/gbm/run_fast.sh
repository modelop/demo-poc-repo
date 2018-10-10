#!/bin/bash
fastscore use engine-2
fastscore engine reset
fastscore run auto_gbm gbm_file_input gbm_output_kafka
python3 ../kafka_1.py
