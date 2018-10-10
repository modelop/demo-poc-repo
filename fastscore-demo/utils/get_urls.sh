#!/bin/bash
HOSTNAME=`hostname`
echo "=======FastScore URLs======="
echo "Dashboard URL:"
echo "https://${HOSTNAME}:7999" 
echo "Model Deploy-1 URL:"
docker service logs fastscore_model-deploy-1 2>&1 | grep localhost | awk '{print $3}' | sed -e s/localhost/${HOSTNAME}/
echo "Model Deploy-2 URL:"
docker service logs fastscore_model-deploy-2 2>&1 | grep localhost | awk '{print $3}' | sed -e s/localhost/${HOSTNAME}/ | sed -e s/8888/8889/
echo "============================"
