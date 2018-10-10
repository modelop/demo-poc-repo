# alerts when prediction differs from observation by a certain threshold

# fastscore.schema.0: double
# fastscore.schema.2: double
# fastscore.schema.1: string

def begin():
    global obs, preds
    obs = []
    preds = []

def action(data, slot):
    global obs, preds, lag

    if slot == 0:
        preds.append(data)
    if slot == 2:
        obs.append(data)
    while len(obs) > 0 and len(preds) > 0:
        observed = obs[0]
        predicted = preds[0]
        obs = obs[1:]
        preds = preds[1:]

        diff = abs(observed - predicted)
        if diff > 5: # more than $5 off the actual close price
            yield "{} [WARN] Observed: {} Error: {}".format(predicted, observed, diff)
        else:
            yield "{}".format(predicted)
