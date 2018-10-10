# fastscore.schema.0: report

# fastscore.schema.1: tagged-double

 

# fastscore.schema.2: enginestate

 

import requests

import json

 

def find_id(engine_host):

    return json.loads(requests.get(f'https://{engine_host}:8003/1/health',verify=False).text)['id']

 

def begin():

    global ENGINE_ID, ENGINE_NAME, M_NAME, WORKFLOW_NAME, OLD_COUNTS

    M_NAME = 'muniai-clustering'

    ENGINE_NAME = 'engine-1'

    ENGINE_ID = find_id(ENGINE_NAME)

    OLD_COUNTS = {}

 

def make_record(name, value):

    return {

        'name': name,

        'value': value

    }

 

def action(datum, slotno):

    global OLD_COUNTS

 

    if slotno == 2:

        if datum['src'] == ENGINE_ID:

            if datum['state'] == 'running':

                yield (1, make_record('{}.engine.state'.format(M_NAME), -1.0))

            elif datum['state'] == 'error':

                yield (1, make_record('{}.engine.state'.format(M_NAME), 1.0))

    else:

       if datum['src'] == ENGINE_ID:

            if datum['tap'] == 'manifold.0.records.count':

                yield (1, make_record('{}.input.count'.format(M_NAME), float(datum['data'])))

 

                try:

                    old_n = OLD_COUNTS['{}.input'.format(M_NAME)]

                   

                    delta_n = datum['data'] - old_n

 

                    if datum['delta_time'] != 0:

                        try:

                            yield (1, make_record('{}.input.rps'.format(M_NAME), float(abs(delta_n / OLD_COUNTS['{}.delta'.format(MODEL_NAME)]))))

                        except Exception as e:

                            pass

                        OLD_COUNTS['{}.delta'.format(M_NAME)] = datum['delta_time']

                    else:

                       OLD_COUNTS['{}.input'.format(M_NAME)] += datum['data']

                except Exception as e:

                    OLD_COUNTS['{}.input'.format(M_NAME)] = datum['data']

            elif datum['tap'] == 'manifold.1.records.count':

                yield (1, make_record('{}.output.count'.format(M_NAME), float(datum['data'])))

 

                try:

                    old_n = OLD_COUNTS['{}.output'.format(M_NAME)]

                    delta_n = datum['data'] - old_n

 

                    if datum['delta_time'] != 0:

                        try:

                            yield (1, make_record('{}.output.rps'.format(M_NAME), float(abs(delta_n / OLD_COUNTS['{}.delta'.format(MODEL_NAME)]))))

                        except Exception as e:

                            pass

                        OLD_COUNTS['{}.delta'.format(M_NAME)] = datum['delta_time']

                    else:

                        OLD_COUNTS['{}.output'.format(M_NAME)] += datum['data']

                except Exception as e:

                    OLD_COUNTS['{}.output'.format(M_NAME)] = datum['data']

            elif datum['tap'] == 'sys.memory':

                yield (1, make_record('{}.memory.usage'.format(M_NAME), float(datum['data'])))

            elif datum['tap'] == 'sys.cpu.utilization':

                yield (1, make_record('{}.cpu.utilization'.format(M_NAME), float(datum['data'])))
