# fastscore.schema.0: double
# fastscore.schema.2: adjustment
# fastscore.schema.1: double

def begin():
    global adjustments, predictions
    adjustments = []
    predictions = []

def action(data, slot):
    global adjustments, predictions

    if slot == 0:
        predictions.append(data)
    if slot == 2:
        adjustments.append(data)

    while len(adjustments) > 0 and len(predictions) > 0:
        adjust = adjustments[0]
        pred = predictions[0]
        adjustments = adjustments[1:]
        predictions = predictions[1:]

        lr = adjust['LR']
        cpi = adjust['CPI']

        yield cpi*(pred + lr)
