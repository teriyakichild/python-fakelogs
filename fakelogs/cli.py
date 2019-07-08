import json
import logging
import os
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
    return config

def generate_text_log():
    Factory = Faker()
    logging.info(Factory.sentence(nb_words=15))

def generate_kv_log():
    Factory = Faker()
    profile = Factory.profile()
    # The following fields aren't strings so we will remove them to avoid additional processing.
    del profile['current_location']
    del profile['website']
    logging.info(' '.join(['{0}={1}'.format(k,v) for k,v in profile.items()]))

def generate_json_log():
    def json_default(o):
        # Two of the values returned by Faker.profile fail to serialize into json. They are
        # decimal.Decimal and datetime.date.  They both have a __str__ function that we can use
        # to convert the values to a strings.
        return o.__str__()

    Factory = Faker()
    logging.info(json.dumps(Factory.profile(), default=json_default))

def main():
    config = read_from_environment()
    log_generators = {
        'text': generate_text_log,
        'kv': generate_kv_log,
        'json': generate_json_log,
    }
    pool = Pool(processes=4)
    while True:
        multiple_results = [pool.apply_async(log_generators[config['OUTPUT_FORMAT']], ()) for i in range(config['RECORDS_PER_ITERATION'])]
        time.sleep(config['TIME_TO_SLEEP'])
