# -*- coding: utf-8 -*-
import pytest
import json as JSON

from opus.data import DataDict, Data, DataElement


@pytest.fixture
def data_dict():
    return DataDict()

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/data.json', 'r').read())

@pytest.fixture
def data(json):
    return Data(json)

@pytest.fixture
def el(data):
    return data['COISS_2016-1508054834_1508117267-N1508094647_1']


def test_data_dict(data_dict):
    data_dict.load({'abc': 'foo', 'def': 'bar'})
    assert repr(data_dict) == '<OPUS API generic class for data objects>'
    assert len(data_dict) == 2
    assert data_dict['abc'] == 'foo'
    assert data_dict['def'] == 'bar'

def test_data_dict_find(data_dict):
    data_dict.load({'abc': 'foo', 'def': 'bar'})
    assert 'abc' in data_dict.find('AB')
    assert data_dict.find('ac') is None

def test_data_dict_iter(data_dict):
    data_dict.append('abc', 'foo')

    for key in data_dict:
        assert key == 'abc'

    for key in data_dict.keys():
        assert key == 'abc'

    for key, value in data_dict.items():
        assert key == 'abc'
        assert value == 'foo'

    for value in data_dict.values():
        assert value == 'foo'


def test_data_meta(data):
    r = repr(data)
    assert 'OPUS API Data objects (with 10 elements)' in r
    assert 'COISS_2016-1509692161_1509948012-N1509868439_1' in r
    assert data.count == 10
    assert data.limit == 10
    assert data.page_no == 2
    assert data.order == 'time1,opusid'


def test_data_labels(data):
    labels = data.labels
    assert labels[0] == 'OPUS ID'
    assert labels[1] == 'Instrument Name'
    assert labels[2] == 'Planet'
    assert labels[3] == 'Intended Target Name'
    assert labels[4] == 'Observation Start Time (UTC)'
    assert labels[5] == 'Observation Duration'


def test_data_element(el):
    assert 'Planet' in repr(el)
    assert el['Instrument Name'] == "Cassini ISS"
    assert el['Planet'] == "Saturn"
    assert el['Intended Target Name'] == "Pan"
    assert el['Observation Start Time (UTC)'] == "2005-10-15T18:42:08.622"
    assert el['Observation Duration'] == 0.68
    assert len(el) == 5


def test_data_element_err():
    with pytest.raises(KeyError):
        DataElement(['abc'], ['foo'])
