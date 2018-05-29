# -*- coding: utf-8 -*-
import json as JSON
import pytest
import six


from opus.fields import *


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

def test_field_repr(field):
    assert repr(field) == \
        '`target` -> Intended Target Name\n' + \
        'The target_name element identifies a target. The target may be a planet, ' + \
        'satellite,ring,region, feature, asteroid or comet. See target_type.\n' + \
        '_More info_: http://pds-rings.seti.org/dictionary/index.php?term=TARGET_NAME&context=PSDD'

def test_field_empty(field_empty):
    assert repr(field_empty) == '`empty` -> Empty'
    assert field_empty.url == None

def test_field_err(field):
    with pytest.raises(KeyError):
        Field('abc', {})

def test_split_key():
    assert splitKey('surfacegeometryTITANIAsubobserverIAUlongitude') == ('TITANIA', 'subobserverIAUlongitude')

def test_fields_repr(fields):
    assert repr(fields) == 'OPUS API list of all fields (3971)'
    
def test_fields_iter(fields):
    assert 'GLOBAL' in fields
    
    for key, value in fields.items():
        assert fields[key] == value
        break

def test_fields_keys_values(fields):
    keys = fields.keys()
    values = fields.values()
    assert len(keys) == 304
    assert len(values) == 304
    assert 'GLOBAL' in keys
    assert 'JUPITER' in keys


def test_global_field_repr(fields):
    assert isinstance(repr(fields['global']), str)
    assert len(fields['global'].values()) == 234

def test_global_field_iter(fields):
    assert 'line1' in fields['global']
    assert repr(fields['global']['line1']) == '`LINE1` -> Line'

def test_surface_geometry_repr(fields):
    if six.PY3:
        assert repr(fields['jupiter']) == \
            'OPUS API Surface Geometry fields (31) for `Jupiter`:\n' + \
            ' - Solar Hour Angle (solarhourangle)\n' + \
            ' - Body Center Resolution (centerresolution)\n' + \
            ' - Observed Phase Angle 2 (phase2)\n' + \
            ' - Observed Phase Angle (phase1)\n' + \
            ' - Coarsest Observed Resolution (coarsestresolution1)\n' + \
            ' - Sub-Solar IAU West Longitude (subsolarIAUlongitude)\n' + \
            ' - Observed Incidence Angle (incidence1)\n' + \
            ' - D Solar Hour Angle (dsolarhourangle)\n' + \
            ' - Observed Planetocentric Latitude 2 (planetocentriclatitude2)\n' + \
            ' - Body Center Distance (centerdistance)\n' + \
            ' - D Observer Longitude (dObserverlongitude)\n' + \
            ' - Sub-Solar Planetographic Latitude (subsolarplanetographiclatitude)\n' + \
            ' - Sub-Observer Planetocentric Latitude (subobserverplanetocentriclatitude)\n' + \
            ' - Observed Planetographic Latitude (planetographiclatitude1)\n' + \
            ' - Observed Planetographic Latitude 2 (planetographiclatitude2)\n' + \
            ' - Sub-Solar Planetocentric Latitude (subsolarplanetocentriclatitude)\n' + \
            ' - Observed Emission Angle (emission1)\n' + \
            ' - Observed Emission Angle 2 (emission2)\n' + \
            ' - Observed Incidence Angle 2 (incidence2)\n' + \
            ' - Sub-Observer Planetographic Latitude (subobserverplanetographiclatitude)\n' + \
            ' - Coarsest Observed Resolution 2 (coarsestresolution2)\n' + \
            ' - Sub-Observer IAU West Longitude (subobserverIAUlongitude)\n' + \
            ' - Observed Distance to Surface 2 (rangetobody2)\n' + \
            ' - Observed Distance to Surface (rangetobody1)\n' + \
            ' - Observed Local Time 2 (solarhourangle2)\n' + \
            ' - Observed Local Time (solarhourangle1)\n' + \
            ' - Phase Angle at Body Center (centerphaseangle)\n' + \
            ' - Observed Planetocentric Latitude (planetocentriclatitude1)\n' + \
            ' - D Iau West Longitude (dIAUwestlongitude)\n' + \
            ' - Finest Observed Resolution 2 (finestresolution2)\n' + \
            ' - Finest Observed Resolution (finestresolution1)'
    else:
        assert isinstance(repr(fields['jupiter']), str)

def test_surface_geometry_keys(fields):
    keys = fields['jupiter'].keys()
    assert len(keys) == 31
    assert 'solarhourangle' in keys


def test_surface_geometry_find(fields):
    found = fields['jupiter'].find('phase')
    assert len(found) == 3
    assert 'phase1' in found
    assert 'phase2' in found
    assert 'centerphaseangle' in found

    assert fields['jupiter'].find('target') == None
