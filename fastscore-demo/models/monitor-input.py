# fastscore.schema.0: cpi
# fastscore.action.0: input_cpi

# fastscore.schema.2: close
# fastscore.action.2: input_close

# fastscore.schema.1: cpi
# fastscore.schema.3: close

# fastscore.schema.5: tagged-double

def begin():
    global count, prev_cpi, prev_close
    count = {
        'cpi': 0,
        'cpi_filtered': 0,
        'close': 0,
        'close_filtered': 0,
        'total': 0
    }
    prev_cpi = prev_close = None

def make_record(name, value):
    return {
        'name': name,
        'value': value
    }

def input_cpi(datum):
    global count, prev_cpi
    count['total'] += 1
    if prev_cpi is None:
            prev_cpi = datum['CPI']
            count['cpi'] += 1
            if count['total'] % 100 == 0:
                yield (5, make_record('input.total.count', float(count['total'])))
                yield (5, make_record('input.cpi.count', float(count['cpi'])))
            yield (1, datum)
        else:
            if datum['CPI'] // prev_cpi == 1:
                count['cpi'] += 1
                if count['total'] % 100 == 0:
                    yield (5, make_record('input.total.count', float(count['total'])))
                    yield (5, make_record('input.cpi.count', float(count['cpi'])))
                yield (1, datum)
            else:
                count['cpi_filtered'] += 1
                if count['total'] % 100 == 0:
                    yield (5, make_record('input.total.count', float(count['total'])))
                    yield (5, make_record('input.cpi_filtered.count', float(count['close_filtered'])))

def input_close(datum):
    global count, prev_close
    count['total'] += 1
    if prev_close is None:
            prev_close = datum['Close']
            count['close'] += 1
            if count['total'] % 100 == 0:
                yield (5, make_record('input.total.count', float(count['total'])))
                yield (5, make_record('input.close.count', float(count['close'])))
            yield (3, datum)
        else:
            if datum['Close'] // prev_close == 1:
                count['close'] += 1
                if count['total'] % 100 == 0:
                    yield (5, make_record('input.total.count', float(count['total'])))
                    yield (5, make_record('input.close.count', float(count['close'])))
                yield (3, datum)
            else:
                count['close_filtered'] += 1
                if count['total'] % 100 == 0:
                    yield (5, make_record('input.total.count', float(count['total'])))
                    yield (5, make_record('input.close_filtered.count', float(count['close_filtered'])))