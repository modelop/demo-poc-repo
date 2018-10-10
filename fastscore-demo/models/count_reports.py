## Count_reports

# fastscore.schema.0: tagged-report
# fastscore.schema.1: tagged-double

def init_filters():
    global filters
    filters = [
        {
            'type': 'sensor-report',
            'tap': 'manifold.0.records.rejected.by.schema',
            'name': 'input.rejected.count'
        }
    ]

def begin():
    global counts
    init_filters()
    counts = {}
    for f in filters:
        counts[f['name']] = 0


def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def filtered(msg):
    name = None
    for f in filters:
        matched = True
        for key in f:
            if key != 'name' and msg['msg'][key] != f[key]:
                break
        if matched:
            name = f['name']
    return name

def action(datum):
    global counts

    name = filtered(datum)

    if not name is None:
        counts[name] += 1
        yield (1, make_record('{}.{}'.format(datum['model'], name), counts[name]))
