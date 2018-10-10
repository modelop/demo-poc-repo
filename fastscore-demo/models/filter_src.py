## Filter src: splits the input into n outputs based on source
# fastscore.schema.0: report
# fastscore.schema.2: config
# fastscore.action.2: config

# fastscore.slot.1: in-use
# fastscore.slot.3: in-use
# fastscore.slot.5: in-use
# fastscore.slot.7: in-use
# fastscore.schema.$out: tagged-report




import requests
import json

def begin():
    global WORKFLOW_NAME, COMPOSER_HOST, CONFIGURED
    WORKFLOW_NAME = None
    COMPOSER_HOST = None
    CONFIGURED = False

def discover():
    global SRC_TO_MODEL
    SRC_TO_MODEL = {}
    fleet = json.loads(requests.get('https://{}:8010/1/workflow/{}/status'.format(COMPOSER_HOST, WORKFLOW_NAME), verify=False).text)
    idx = 1
    for model in fleet:
        SRC_TO_MODEL[fleet[model]["Engine"]["ID"]] = { "slot": idx, "model": model }
        idx += 2

## CONF: {"item": "conf_name", "value": "conf_value"}
def config(conf):
    global WORKFLOW_NAME, COMPOSER_HOST, CONFIGURED

    if conf["item"] == "workflow_name":
        WORKFLOW_NAME = conf["value"]
    elif conf["item"] == "composer_host":
        COMPOSER_HOST = conf["value"]

    if not (COMPOSER_HOST is None or WORKFLOW_NAME is None):
        discover()
        CONFIGURED = True

def action(datum):
    if CONFIGURED:
        if datum["src"] in SRC_TO_MODEL:
            entry = SRC_TO_MODEL[datum["src"]]
            yield (entry["slot"], { "model": entry["model"], "msg": datum })
