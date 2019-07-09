import json
import logging
import os
import random
import sys
import time

from faker import Faker
from multiprocessing import Pool
from fakelogs.log import generate_text_log, generate_kv_log, generate_json_log


def read_from_environment():
    config = {}
    config['OUTPUT_FORMAT'] = os.getenv('OUTPUT_FORMAT', 'text')
    config['TIME_TO_SLEEP'] = float(os.getenv('TIME_TO_SLEEP', 1))
    config['RECORDS_PER_ITERATION'] = int(os.getenv('RECORDS_PER_ITERATION', 1))
    config['POOL_PROCESSES'] = int(os.getenv('POOL_PROCESSES', 1))
    return config

def main():
    config = read_from_environment()
    log_generators = {
        'text': generate_text_log,
        'kv': generate_kv_log,
        'json': generate_json_log,
    }
    pool = Pool(processes=config['POOL_PROCESSES'])
    while True:
        for i in range(config['RECORDS_PER_ITERATION']):
            # call the log generator function asynchronously with generating the Faker seed with:
            # random.randint(1,4000) + the iterator number
            # This ensures that each call returns different data
            pool.apply_async(log_generators[config['OUTPUT_FORMAT']], (random.randint(1,10000)+i,))
        while not pool._inqueue.empty():
            time.sleep(0.1)
        time.sleep(config['TIME_TO_SLEEP'])
