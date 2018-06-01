# -*- coding: utf-8 -*-
import pytest
import six
import json as JSON

from opus.mults import Mults


@pytest.fixture
def mults():
    json = JSON.loads(open('tests/api/meta/mults/target.json', 'r').read())
    return Mults(json)

def test_mults(mults):
    r = repr(mults)
    assert 'OPUS API Multiple choice for field: `target`' in r
    assert 'TITAN' in r
    assert len(mults) == 63
