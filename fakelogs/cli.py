import json
import logging
from multiprocessing import Pool
import os
import random
import sys
import time
import uuid

from faker import Faker
from fakelogs.log import generate_text_log, generate_kv_log, generate_json_log


def read_from_environment():
    config = {}
    config['OUTPUT_FORMAT'] = os.getenv('OUTPUT_FORMAT', 'text')
    config['TIME_TO_SLEEP'] = float(os.getenv('TIME_TO_SLEEP', 1))
    config['RECORDS_PER_ITERATION'] = int(os.getenv('RECORDS_PER_ITERATION', 1))
    config['POOL_PROCESSES'] = int(os.getenv('POOL_PROCESSES', 1))
    config['MAX_ITERATIONS'] = int(os.getenv('MAX_ITERATIONS', False))
    config['TRANSACTION_ID'] = str(os.getenv('TRANSACTION_ID', uuid.uuid4()))
    config['PRELOAD_DATA'] = bool(os.getenv('PRELOAD_DATA', False))
    config['PRELOAD_RECORDS'] = int(os.getenv('PRELOAD_RECORDS', 2000))
    return config

def main():
    config = read_from_environment()
    if '--help' in sys.argv or '-h' in sys.argv:
        print('Usage:\n {0}\n {0} [-h|--help]\n {0} [--show-config]'.format(sys.argv[0]))
        exit(0)
    elif '--show-config' in sys.argv:
        print(json.dumps(config, indent=2))
        exit(0)
    log_generators = {
        'text': generate_text_log,
        'kv': generate_kv_log,
        'json': generate_json_log,
    }
    pool = Pool(processes=config['POOL_PROCESSES'])
    if config['PRELOAD_DATA']:
        logging.info('Generating dataset..')
        dataset = []
        def callback(result):
            dataset.append(result)
        # Generate the dataset
        for i in range(config['PRELOAD_RECORDS']):
            # random.randint uses the current time to generate the return.  When POOL_PROCESSES
            # is set greater than 1, the log_generator function is called multiple times
            # concurrently. This results in outputting sets of identical log records.
            # To avoid this, we add the iteration index to the random number.
            seed = random.randint(1,10000) + i
            pool.apply_async(log_generators[config['OUTPUT_FORMAT']], (seed,config['TRANSACTION_ID'],True), callback=callback)
        # wait until all the queued logs are generated
        while not pool._inqueue.empty():
            time.sleep(0.1)
        iterations = 0
        while True:
            for i in range(config['RECORDS_PER_ITERATION']):
                iterations += 1
                logging.info(dataset[random.randint(1,(config['PRELOAD_RECORDS'] - 1))])
            time.sleep(config['TIME_TO_SLEEP'])
            if config['MAX_ITERATIONS']:
                if iterations >= config['MAX_ITERATIONS']:
                    logging.info('Maximum number of iterations hit. Quitting..')
                    exit(0)
    else:
        iterations = 0
        while True:
            iterations += 1
            for i in range(config['RECORDS_PER_ITERATION']):
                # random.randint uses the current time to generate the return.  When POOL_PROCESSES
                # is set greater than 1, the log_generator function is called multiple times
                # concurrently. This results in outputting sets of identical log records.
                # To avoid this, we add the iteration index to the random number.
                seed = random.randint(1,10000) + i
                pool.apply_async(log_generators[config['OUTPUT_FORMAT']], (seed,config['TRANSACTION_ID']))

            # wait until all the queued logs are generated
            while not pool._inqueue.empty():
                time.sleep(0.1)
            time.sleep(config['TIME_TO_SLEEP'])
            if config['MAX_ITERATIONS']:
                if iterations >= config['MAX_ITERATIONS']:
                    logging.info('Maximum number of iterations hit. Quitting..')
                    exit(0)
