# -*- coding: utf-8 -*-
import json as JSON
import pytest

from opus.categories import Categories, Category

@pytest.fixture
def category():
    json = JSON.loads(open('tests/api/categories/obs_general.json', 'r').read())
    return Category(json)

@pytest.fixture
def categories():
    json = JSON.loads(open('tests/api/categories.json', 'r').read())
    return Categories(json)

def test_category_repr(category):
    assert repr(category) == 'General Constraints (obs_general)'


def test_categories_repr(categories):
    r = repr(categories)
    assert 'OPUS API list of all categories (3)' in r
    assert 'General Constraints (obs_general)' in r
