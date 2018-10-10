# fastscore.schema.1: string
# fastscore.schema.3: tagged-double
# fastscore.schema.0: double

def begin():
    global THRESHOLD, COUNT
    THRESHOLD = 30
    COUNT = 0

def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def action(datum):
   global COUNT 
   if datum > THRESHOLD:
        COUNT += 1
        yield (1, 'Threshold monitor triggered: {} > {}'.format(datum, THRESHOLD))
        yield (3, make_record('monitor.threshold.count', COUNT))
