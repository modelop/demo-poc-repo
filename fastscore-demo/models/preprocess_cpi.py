# fastscore.schema.0: cpi
# fastscore.schema.1: cpi
# fastscore.schema.3: alert
# fastscore.action.0: preprocess

def begin():
    global count
    count = 0

def make_alert(datum):
    import json
    return {
        'src': 'input-preprocess',
        'name': 'preprocess-cpi',
        'value': json.dumps(datum)
    }

def preprocess(datum):
    global count
    count += 1
    yield (1, datum)
    if count % 10 == 0:
        yield (3, make_alert(datum))