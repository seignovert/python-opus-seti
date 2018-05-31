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
    return data['S_IMG_CO_ISS_1508094647_N']


def test_data_dict(data_dict):
    data_dict.load({'abc': 'foo', 'def': 'bar'})
    assert repr(data_dict) == '<OPUS API generic class for data objects>'
    assert len(data_dict) == 2
    assert data_dict['abc'] == 'foo'
    assert data_dict['def'] == 'bar'


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
    assert 'S_IMG_CO_ISS_1508094647_N' in r
    assert data.count == 10
    assert data.limit == 10
    assert data.page_no == 2
    assert data.order == 'obs_general.time1'


def test_data_labels(data):
    labels = data.labels
    assert labels[0] == 'Ring Observation ID'
    assert labels[1] == 'Planet'
    assert labels[2] == 'Intended Target Name'
    assert labels[3] == 'Observed Phase Angle (Min)'
    assert labels[4] == 'Observed Phase Angle (Max)'
    assert labels[5] == 'Observation Start Time (UTC)'
    assert labels[6] == 'Observation Stop Time (UTC)'


def test_data_element(el):
    assert 'Planet' in repr(el)
    assert el['Planet'] == 'SAT'
    assert el['Intended Target Name'] == 'PAN'
    assert el['Observed Phase Angle (Min)'] == 87.786
    assert el['Observed Phase Angle (Max)'] == 88.169
    assert el['Observation Start Time (UTC)'] == '2005-288T18:42:08.622'
    assert el['Observation Stop Time (UTC)'] == '2005-288T18:42:09.302'
    assert len(el) == 6


def test_data_element_err():
    with pytest.raises(KeyError):
        DataElement(['abc'], ['foo'])
