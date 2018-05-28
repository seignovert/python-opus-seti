# -*- coding: utf-8 -*-
import pytest
import six
import json as JSON

from opus.mults import Mults


@pytest.fixture
def mults():
    json = JSON.loads(open('tests/api/meta/mults/target.json', 'r').read())
    return Mults(json)

def test_mults_meta(mults):
    assert repr(mults) == 'OPUS API Mults for field: target'

def test_mults_getitem(mults):
    assert mults['RHEA'] == 20974

def test_mults_iter(mults):
    for key in mults:
        assert isinstance(key, six.text_type)

def test_mults_keys(mults):
    for key in mults.keys():
        assert isinstance(key, six.text_type)

def test_mults_items(mults):
    for key, value in mults.items():
        assert mults[key] == value

def test_mults_values(mults):
    for value in mults.values():
        assert isinstance(value, int)

def test_mults_getitem_err(mults):
    with pytest.raises(KeyError):
        mults['ABC']
