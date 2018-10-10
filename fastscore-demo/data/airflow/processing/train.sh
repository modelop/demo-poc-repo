#!/bin/bash

fastscore connect https://dashboard:8000
fastscore -wait fleet
cd /usr/local/airflow/processing
fastscore model add -type:python3 lr-2 lr_model_2.py3
fastscore attachment upload lr-2 lr_pickle2.tar.gz
