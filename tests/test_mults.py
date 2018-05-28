# -*- coding: utf-8 -*-
import pytest
import six
import json as JSON

from opus.mults import Mults


@pytest.fixture
def mutls():
    json = JSON.loads(open('tests/api/meta/mults/target.json', 'r').read())
    return Mults(json)

def test_mults_meta(mutls):
    assert repr(mutls) == 'OPUS API Mults for field: target'

def test_mults_getitem(mutls):
    assert mutls['RHEA'] == 20974

def test_mults_iter(mutls):
    for key in mutls:
        assert isinstance(key, six.text_type)

def test_mults_keys(mutls):
    for key in mutls.keys():
        assert isinstance(key, six.text_type)

def test_mults_items(mutls):
    for key, value in mutls.items():
        assert mutls[key] == value

def test_mults_values(mutls):
    for value in mutls.values():
        assert isinstance(value, int)

def test_mults_getitem_err(mutls):
    with pytest.raises(KeyError):
        mutls['ABC']
