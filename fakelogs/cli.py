import json
import logging
import os
import time

from faker import Faker

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def read_from_environment():
    config = {}
    config['OUTPUT_FORMAT'] = os.getenv('OUTPUT_FORMAT', 'text')
    config['TIME_TO_SLEEP'] = int(os.getenv('TIME_TO_SLEEP', 1))
    config['RECORDS_PER_ITERATION'] = int(os.getenv('RECORDS_PER_ITERATION', 1))
    return config

def generate_text_log():
    Factory = Faker()
    logging.warning(Factory.text())

def generate_kv_log():
    Factory = Faker()
    profile = Factory.profile()
    # The following fields aren't strings so we will remove them to avoid additional processing.
    del profile['current_location']
    del profile['website']
    logging.warning(' '.join(['{0}={1}'.format(k,v) for k,v in profile.items()]))

def generate_json_log():
    def json_default(o):
        # Two of the values returned by Faker.profile fail to serialize into json. They are
        # decimal.Decimal and datetime.date.  They both have a __str__ function that we can use
        # to convert the values to a strings.
        return o.__str__()

    Factory = Faker()
    logging.warning(json.dumps(Factory.profile(), default=json_default))

def main():
    config = read_from_environment()
    log_generators = {
        'text': generate_text_log,
        'kv': generate_kv_log,
        'json': generate_json_log,
    }

    while True:
        for _ in range(config['RECORDS_PER_ITERATION']):
            log_generators[config['OUTPUT_FORMAT']]()
        time.sleep(config['TIME_TO_SLEEP'])
