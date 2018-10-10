## Count alerts

# fastscore.schema.0: alert
# fastscore.schema.1: tagged-double

def begin():
    global COUNTS
    COUNTS = {}


def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def action(datum):
    global COUNTS

    try:
        COUNTS[datum['name']] += 1
    except Exception as e:
        COUNTS[datum['name']] = 1
    
    yield (1, make_record(datum['name'], float(COUNTS[datum['name']])))
