# -*- coding: utf-8 -*-
import pytest

import json as JSON

from opus.fields import Field


@pytest.fixture
def field():
    json = JSON.loads(open('tests/api/fields/target.json', 'r').read())
    return Field('target', json)

def test_field_repr(field):
    assert repr(field) == \
        '`target` -> Intended Target Name\n' + \
        'The target_name element identifies a target. The target\n' + \
        '   may be a planet, satellite,ring,region, feature,\n' + \
        '   asteroid or comet. See target_type.\n\n' + \
        'More info: http://pds-rings.seti.org/dictionary/index.php?term=TARGET_NAME&context=PSDD'

def test_field_err(field):
    with pytest.raises(KeyError):
        Field('abc', {})
