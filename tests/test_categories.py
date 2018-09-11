# -*- coding: utf-8 -*-
import json as JSON
import pytest

from opus.categories import Categories, Category

@pytest.fixture
def category():
    json = JSON.loads(open('tests/api/categories/COISS_2001-1459551663_1459568594-N1459551972_1.json', 'r').read())
    return Categories(json)

@pytest.fixture
def categories():
    json = JSON.loads(open('tests/api/categories.json', 'r').read())
    return Categories(json)

def test_category_repr(category):
    r = repr(category)
    assert 'OPUS API list of all categories (8)' in r
    assert 'Cassini ISS Constraints (obs_instrument_coiss)' in r


def test_categories_repr(categories):
    r = repr(categories)
    assert 'OPUS API list of all categories (6)' in r
    assert 'Ring Geometry Constraints (obs_ring_geometry)' in r
