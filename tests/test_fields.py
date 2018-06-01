# -*- coding: utf-8 -*-
import pytest
import json as JSON

from opus.fields import Fields, Field, splitKey

@pytest.fixture
def field():
    json = JSON.loads(open('tests/api/fields/target.json', 'r').read())
    return Field('target', json['target'])

@pytest.fixture
def fields():
    json = JSON.loads(open('tests/api/fields.json', 'r').read())
    return Fields(json)

@pytest.fixture
def field_empty():
    return Field('empty', {'label': 'Empty', 'more_info': {'def': False, 'more_info': False}})

def test_split_key():
    assert splitKey('surfacegeometryTITANIAsubobserverIAUlongitude') == ('TITANIA', 'subobserverIAUlongitude')

def test_field_repr(field):
    assert repr(field) == 'Intended Target Name (target):\n' + \
        ' => The target_name element identifies a target. The target may be a planet, satellite,ring,region, feature, asteroid or comet. See target_type.\n' + \
        ' http://pds-rings.seti.org/dictionary/index.php?term=TARGET_NAME&context=PSDD'
    assert str(field) == 'Intended Target Name'

def test_field_empty(field_empty):
    assert repr(field_empty) == 'Empty: (empty)'
    assert field_empty.url == None

def test_field_err(field):
    with pytest.raises(KeyError):
        Field('abc', {})

def test_fields_repr(fields):
    r = repr(fields)
    assert 'OPUS API list of all fields available (304)' in r
    assert 'GLOBAL' in r
    
def test_global_field_repr(fields):
    r = repr(fields['GLOBAL'])
    assert 'OPUS API Global fields (234)' in r
    assert 'Lesser Size in Pixels' in r


def test_surface_geometry_repr(fields):
    r = repr(fields['TITAN'])
    assert 'OPUS API Surface Geometry fields (31) for `Titan`' in r
    assert 'Sub-Solar IAU West Longitude' in r
    
