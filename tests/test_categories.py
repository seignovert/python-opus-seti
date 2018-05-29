# -*- coding: utf-8 -*-
import json as JSON
import pytest
import six

from opus.categories import *

@pytest.fixture
def category():
    json = JSON.loads(open('tests/api/category/obs_general.json', 'r').read())
    return Category(json)

@pytest.fixture
def categories():
    json = JSON.loads(open('tests/api/categories.json', 'r').read())
    return Categories(json)

def test_category_repr(category):
    assert repr(category) == '`obs_general` -> General Constraints'


def test_categories_repr(categories):
    if six.PY3:
        assert repr(categories) == \
            'OPUS API list of all categories (3):\n' + \
            ' - General Constraints (obs_general)\n' + \
            ' - Ring Geometry Constraints (obs_ring_geometry)\n' + \
            ' - Wavelength Constraints (obs_wavelength)'
    else:
        r = repr(categories)
        assert 'OPUS API list of all categories (3):' in r
        assert 'obs_general' in r
        assert 'obs_ring_geometry' in r
        assert 'obs_wavelength' in r
    
def test_categories_iter(categories):
    assert 'obs_general' in categories
    
    for key, value in categories.items():
        assert categories[key] == value
        break

def test_categories_keys_values(categories):
    keys = categories.keys()
    values = categories.values()
    assert len(keys) == 3
    assert len(values) == 3
    assert 'obs_general' in keys


