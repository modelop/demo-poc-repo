#!/bin/bash
HOSTNAME=localhost
echo Configuring FastScore...
echo fastscore connect https://${HOSTNAME}:7999
fastscore connect https://${HOSTNAME}:7999
echo fastscore config set config.yaml
fastscore config set config.yaml
echo Checking fleet status...
echo fastscore fleet
fastscore -wait fleet
