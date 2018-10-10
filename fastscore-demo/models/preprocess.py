# fastscore.schema.0: int
# fastscore.schema.1: int
# fastscore.schema.3: alert
# fastscore.action.0: preprocess


def make_alert(datum):
    return {
        'src': 'preprocess',
        'value': datum
    }

def preprocess(datum):
    try:
        datum == int(datum)
        yield (1, datum)
    except Exception as e:
        yield (3, make_alert(datum))