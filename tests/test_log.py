import json
import os

import pytest
from fakelogs.log import generate_text_log, generate_kv_log, generate_json_log

def test_generate_text_log(caplog):
    generate_text_log(1234)
    for record in caplog.records:
        assert record.msg == u'Key account treat vote old public base short door air small get perhaps past chance consumer boy address main who. '


def test_generate_text_log_with_more_words(caplog):
    generate_text_log(1234, {'TEXT_WORD_COUNT':20})
    for record in caplog.records:
        assert record.msg == u'Key account treat vote old public base short door air small get perhaps past chance consumer boy address main who ask must letter own become often especially. '


def test_generate_json_log(caplog):
    generate_json_log(1234)
    for record in caplog.records:
        assert json.loads(record.msg)['company'] == 'Smith-Bartlett'


def test_generate_kv_log(caplog):
    generate_kv_log(1234)
    for record in caplog.records:
        assert 'username=hkrueger' in record.msg 
