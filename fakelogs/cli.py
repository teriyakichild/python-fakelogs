import json
import logging
import os
import random
import sys
import time

from faker import Faker
from multiprocessing import Pool

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def read_from_environment():
    config = {}
    config['OUTPUT_FORMAT'] = os.getenv('OUTPUT_FORMAT', 'text')
    config['TIME_TO_SLEEP'] = int(os.getenv('TIME_TO_SLEEP', 1))
    config['RECORDS_PER_ITERATION'] = int(os.getenv('RECORDS_PER_ITERATION', 1))
    config['POOL_PROCESSES'] = int(os.getenv('POOL_PROCESSES', 1))
    return config

def generate_text_log(seed):
    Factory = Faker()
    Factory.seed(seed)
    logging.info(Factory.sentence(nb_words=15))

def generate_kv_log(seed):
    Factory = Faker()
    Factory.seed(seed)
    profile = Factory.profile()
    # The following fields aren't strings so we will remove them to avoid additional processing.
    del profile['current_location']
    del profile['website']
    logging.info(' '.join(['{0}={1}'.format(k,v) for k,v in profile.items()]))

def generate_json_log(seed):
    def json_default(o):
        # Two of the values returned by Faker.profile fail to serialize into json. They are
        # decimal.Decimal and datetime.date.  They both have a __str__ function that we can use
        # to convert the values to a strings.
        return o.__str__()

    Factory = Faker()
    Factory.seed(seed)
    logging.info(json.dumps(Factory.profile(), default=json_default))

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
        time.sleep(config['TIME_TO_SLEEP'])
