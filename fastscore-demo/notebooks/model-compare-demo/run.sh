#!/bin/bash

fastscore fleet

fastscore use engine-3
fastscore stream attach middle1 0
fastscore stream attach middle1 0
fastscore stream attach middle2 2
fastscore stream attach middle2 2
#fastscore stream attach heartbeat 4
fastscore stream attach output 1
fastscore model load model-compare
