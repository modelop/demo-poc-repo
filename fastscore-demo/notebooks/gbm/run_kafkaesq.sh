#!/bin/bash
fastscore use engine-2
fastscore engine reset
fastscore run auto_gbm gbm_input_kafka gbm_output_kafka
../kafkaesq --bootstrap kafka:9092 --input-file gbm_input_data_multiline.json gbm-input model-output
