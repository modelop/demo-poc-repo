#!/bin/bash
fastscore fleet
fastscore schema add hello_input input.avsc
fastscore schema add hello_output output.avsc
fastscore model add hello-world model.py
fastscore stream add rest-in rest-in.json
fastscore stream add rest-out rest-out.json
fastscore job run hello-world rest-in rest-out
fastscore job stop
