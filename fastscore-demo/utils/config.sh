#!/bin/bash
HOSTNAME=`hostname`
echo Configuring FastScore...
echo fastscore connect https://${HOSTNAME}:8000
fastscore connect https://${HOSTNAME}:8000
echo fastscore config set config.yaml
fastscore config set config.yaml
echo Checking fleet status...
echo fastscore fleet
fastscore -wait fleet

echo "Adding Composer assets..."
cd composer

# Add models
fastscore model add -type:python3 tf_sp500_lstm tf_sp500_lstm.py
fastscore attachment upload tf_sp500_lstm attachment.tar.gz

fastscore model add preprocessor preprocessor.R
fastscore model add postprocessor postprocessor.py

fastscore model add alerter alerter.py

# Add streams
fastscore stream add rest rest.json
fastscore stream add kafka_in kafka_in.json
fastscore stream add kafka_out kafka_out.json

# Add schemas
fastscore schema add double double.avsc
fastscore schema add cpi cpi.avsc
fastscore schema add sp500 sp500.avsc
fastscore schema add adjustment adjustment.avsc
fastscore schema add string string.avsc
