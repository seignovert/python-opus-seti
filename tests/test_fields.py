# -*- coding: utf-8 -*-
import pytest
import json as JSON

from opus.fields import Fields, Field, splitKey

@pytest.fixture
def field():
    json = JSON.loads(open('tests/api/fields/target.json', 'r').read())
    return Field('target', json['data']['target'])

@pytest.fixture
def fields():
    json = JSON.loads(open('tests/api/fields.json', 'r').read())
    return Fields(json['data'])

def test_split_key():
    assert splitKey('surfacegeometryTITANIAsubobserverIAUlongitude') == ('TITANIA', 'subobserverIAUlongitude')

def test_field_repr(field):
    assert repr(field) == 'Intended Target Name (target):\n' + \
        ' => Category General Constraints / Slug: target'
    assert str(field) == 'Intended Target Name'

def test_field_err(field):
    with pytest.raises(KeyError):
        Field('abc', {})

def test_fields_repr(fields):
    r = repr(fields)
    assert 'OPUS API list of all fields available (247)' in r
    assert 'planet' in r
    
