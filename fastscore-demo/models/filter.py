# fastscore.schema.0: cpi
# fastscore.schema.1: cpi
# fastscore.schema.3: alert
# fastscore.action.0: filter

def begin():
    global PREV_VAL
    PREV_VAL = None

def make_alert(datum):
    import json
    return {
        'src': 'input-filter',
        'name': 'filter-cpi',
        'value': json.dumps(datum)
    }

def filter(datum):
    global PREV_VAL
    if PREV_VAL is None:
        PREV_VAL = datum['CPI']
        yield(1, datum)
    else:
        if datum['CPI'] // PREV_VAL == 1:
            yield (1, datum)
        else:
            yield (3, make_alert(datum))
