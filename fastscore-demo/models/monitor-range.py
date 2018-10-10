# fastscore.schema.1: string
# fastscore.schema.3: tagged-double
# fastscore.schema.0: double

def begin():
    global LOWER, UPPER, COUNT
    LOWER = 10
    UPPER = 40
    COUNT = 0

def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def action(datum):
    global COUNT
    if not datum in range(LOWER, UPPER):
        COUNT += 1
        yield (1, 'Range monitor triggered: {}  outside of ({}, {})'.format(datum, LOWER, UPPER))
        yield (3, make_record('monitor.range.count', COUNT))
