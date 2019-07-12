import os

import pytest
from fakelogs.cli import read_from_environment


def test_read_from_environment_defaults():
    for key in ['OUTPUT_FORMAT', 'TIME_TO_SLEEP', 'RECORDS_PER_ITERATION', 'POOL_PROCESSES']:
        try:
            del os.environ[key]
        except:
            pass
    config = read_from_environment()
    assert config['OUTPUT_FORMAT'] == 'text'
    assert config['TIME_TO_SLEEP'] == 1.0
    assert config['RECORDS_PER_ITERATION'] == 1
    assert config['POOL_PROCESSES'] == 1


def test_read_from_environment_overrides():
    os.environ['OUTPUT_FORMAT'] = 'json'
    os.environ['TIME_TO_SLEEP'] = '2.0'
    os.environ['RECORDS_PER_ITERATION'] = '100'
    os.environ['POOL_PROCESSES'] = '4'
    os.environ['TRANSACTION_ID'] = 'testing'
    config = read_from_environment()
    assert config['OUTPUT_FORMAT'] == 'json'
    assert config['TIME_TO_SLEEP'] == 2.0
    assert config['RECORDS_PER_ITERATION'] == 100
    assert config['POOL_PROCESSES'] == 4
    assert config['TRANSACTION_ID'] == 'testing'

