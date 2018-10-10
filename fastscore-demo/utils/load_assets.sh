fastscore model add -type:python3 influx-mux models/influx.py
fastscore model add -type:python3 process-sensors models/process_sensors.py
fastscore model add -type:python3 lr-1 notebooks/three_models/lr_model.py3
fastscore attachment upload lr-1 lr_pickle1.tar.gz
#fastscore model add -type:python3 lr-2 notebooks/three_models/lr_model.py3
#fastscore model add -type:python3 compute-bound notebooks/three_models/crazy_model.py3
fastscore model add -type:R compute-bound models/crazy_model.R


fastscore schema add report models/report.avsc
fastscore schema add enginestate models/enginestate.avsc
fastscore schema add tagged-double models/tagged-double.avsc
fastscore schema add close_price notebooks/three_models/close_price.avsc
fastscore schema add dubs notebooks/three_models/dubs.avsc

fastscore stream add lr-input-file streams/input_closing.json
fastscore stream add compute-input-file streams/input_compute.json
fastscore stream add compute-output-file streams/output_compute.json
fastscore stream add rest streams/rest.json
fastscore stream add kafka-input streams/input.json
fastscore stream add influx-mux-kafka streams/input_kafka_stream.json
fastscore stream add pneumo-kafka streams/pneumo.json

