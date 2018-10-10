# fastscore.schema.0: close
# fastscore.schema.1: close
# fastscore.schema.3: alert
# fastscore.action.0: filter

def begin():
    global PREV_VAL
    PREV_VAL = None

def make_alert(datum):
    import json
    return {
        'src': 'input-filter',
        'name': 'filter-close',
        'value': json.dumps(datum)
    }

def filter(datum):
    global PREV_VAL
    if PREV_VAL is None:
        PREV_VAL = datum['Close']
        yield(1, datum)
    else:
        if datum['Close'] // PREV_VAL == 1:
            yield (1, datum)
        else:
            yield (3, make_alert(datum))
