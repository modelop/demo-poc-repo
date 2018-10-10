## Cond discard
# fastscore.slot.0: in-use
# fastscore.slot.2: in-use
# fastscore.slot.4: in-use
# fastscore.slot.6: in-use

# fastscore.slot.1: in-use
# fastscore.slot.3: in-use
# fastscore.slot.5: in-use
# fastscore.slot.7: in-use
# fastscore.slot.9: in-use

def begin():
    global THRESHOLD, COUNT
    THRESHOLD = 10000000
    COUNT = 0

def action(datum, slotno):
    global COUNT
    COUNT += 1
    if COUNT < THRESHOLD:
        yield (slotno + 3, datum)
    else:
        yield (1, datum)