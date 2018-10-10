# fastscore.schema.0: tagged-report
# fastscore.schema.1: tagged-double

# rec_acc <- accumulated number of records (with a zero delta)
# old_dt <- first delta in series

def init_filters():
    global filters
    filters = [
        {
            'type': 'sensor-report',
            'tap': 'manifold.1.records.count',
            'name': 'output.rps'
        },
    {
            'type': 'sensor-report',
            'tap': 'manifold.0.records.count',
            'name': 'input.rps'
        }
    ]

def filtered(msg):
    name = None
    for f in filters:
        matched = True
        for key in f:
            if key != 'name' and msg['msg'][key] != f[key]:
                matched = False
        if matched:
            name = f['name']
    return name

def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def begin():
    global rec_acc, old_dt
    init_filters()
    rec_acc = {}
    old_dt = {}
    for f in filters:
        rec_acc[f['name']] = 1
        old_dt[f['name']] = 0

def action(datum):
    global rec_acc, old_dt

    name = filtered(datum)

    if not name is None:
        
        dt = datum['msg']['delta_time']

        if dt == 0: # accumulate
            rec_acc[name] += 1
        else: # flush
            if old_dt[name] == 0: # first record
                yield (1, make_record('{}.{}'.format(datum['model'], name), rec_acc[name] / dt))
            else:
                yield (1, make_record('{}.{}'.format(datum['model'], name), rec_acc[name] / old_dt[name]))
            rec_acc[name] = 1
            old_dt[name] = dt
