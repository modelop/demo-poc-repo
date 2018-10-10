# fastscore.schema.0: double
# fastscore.schema.2: double
# fastscore.schema.1: tagged-double

def begin():
    global count, obs, preds
    count = {
        'score': 0,
        'diverge': 0
    }
    obs = []
    preds = []


def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def action(data, slot):
    global obs, preds, count

    if slot == 0:
        obs.append(data)
    if slot == 2:
        preds.append(data)
    while len(obs) > 0 and len(preds) > 0:
        observed = obs[0]
        predicted = preds[0]
        obs = obs[1:]
        preds = preds[1:]

        diff = abs(observed - predicted)
        if diff > 5: # more than $5 off the actual close price
            count['diverge'] += 1
            yield (1, make_record('output.diverge.count', float(count['diverge'])))
        yield (1, make_record('predicted.value', float(predicted)))
        yield (1, make_record('observed.value', float(observed)))
        yield (1, make_record('predicted.observed.diff', float(observed - predicted)))
    count['score'] += 1
    if count['score'] % 100 == 0:
        yield (1, make_record('output.score.count', float(count['score'])))
