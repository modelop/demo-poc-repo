#!/bin/bash

fastscore fleet

fastscore model add model-compare model-compare.py
fastscore attachment upload model-compare ModelCompare.tar.gz
fastscore stream add middle1 middle1.json
fastscore stream add middle2 middle2.json

fastscore schema add output-schema output.avsc
fastscore stream add output output.json
#fastscore stream add heartbeat heartbeat.json
fastscore schema add double <<EOF
{"type": "double"}
EOF
fastscore schema add string <<EOF
{"type": "string"}
EOF
fastscore use engine-3
fastscore stream attach middle1 0
fastscore stream attach middle1 0
fastscore stream attach middle2 2
fastscore stream attach middle2 2
#fastscore stream attach heartbeat 4
fastscore stream attach output 1
fastscore model load model-compare
