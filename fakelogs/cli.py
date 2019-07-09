import json
import logging
from multiprocessing import Pool
import os
import random
import sys
import time

from faker import Faker
from fakelogs.log import generate_text_log, generate_kv_log, generate_json_log


def read_from_environment():
    config = {}
    config['OUTPUT_FORMAT'] = os.getenv('OUTPUT_FORMAT', 'text')
    config['TIME_TO_SLEEP'] = float(os.getenv('TIME_TO_SLEEP', 1))
    config['RECORDS_PER_ITERATION'] = int(os.getenv('RECORDS_PER_ITERATION', 1))
    config['POOL_PROCESSES'] = int(os.getenv('POOL_PROCESSES', 1))
    config['MAX_ITERATIONS'] = int(os.getenv('MAX_ITERATIONS', False))
    return config

def main():
    config = read_from_environment()
    if '--help' in sys.argv or '-h' in sys.argv:
        print('Usage:\n {0}\n {0} [-h|--help]\n {0} [-c|--show-config]'.format(sys.argv[0]))
        exit(0)
    elif '--show-config' in sys.argv or '-c' in sys.argv:
        print(json.dumps(config, indent=2))
        exit(0)
    log_generators = {
        'text': generate_text_log,
        'kv': generate_kv_log,
        'json': generate_json_log,
    }
    pool = Pool(processes=config['POOL_PROCESSES'])
    iterations = 0
    while True:
        iterations += 1
        for i in range(config['RECORDS_PER_ITERATION']):
            # call the log generator function asynchronously with generating the Faker seed with:
            # random.randint(1,4000) + the iterator number
            # This ensures that each call returns different data
            pool.apply_async(log_generators[config['OUTPUT_FORMAT']], (random.randint(1,10000)+i,))
        while not pool._inqueue.empty():
            time.sleep(0.1)
        time.sleep(config['TIME_TO_SLEEP'])
        if config['MAX_ITERATIONS']:
            if iterations >= config['MAX_ITERATIONS']:
                logging.info('Maximum number of iterations hit. Quitting..')
                exit(0)
