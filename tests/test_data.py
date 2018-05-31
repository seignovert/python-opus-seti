# -*- coding: utf-8 -*-
import pytest

import json as JSON

from opus.data import Data, DataElement

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/data.json', 'r').read())

@pytest.fixture
def data(json):
    return Data(json)

@pytest.fixture
def el(data):
    return data['S_IMG_CO_ISS_1508094647_N']

def test_data_meta(data):
    r = repr(data)
    assert 'OPUS API Data object (with 10 elements)' in r
    assert '- S_IMG_CO_ISS_1508094647_N' in r
    assert len(data) == 10
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


def test_data_iter(data):
    for key in data:
        assert key in data.keys()
        break

    for value in data.values():
        assert isinstance(value, DataElement)
        break


def test_data_element(el):
    assert el['Planet'] == 'SAT'
    assert el['Intended Target Name'] == 'PAN'
    assert el['Observed Phase Angle (Min)'] == 87.786
    assert el['Observed Phase Angle (Max)'] == 88.169
    assert el['Observation Start Time (UTC)'] == '2005-288T18:42:08.622'
    assert el['Observation Stop Time (UTC)'] == '2005-288T18:42:09.302'
    assert len(el) == 6
    assert 'Planet' in repr(el)
    assert 'SAT' in el.values()


def test_data_element_iter(el):
    for key in el:
        assert key in el.keys()
        break

def test_data_element_err():
    with pytest.raises(KeyError):
        DataElement(['abc'], ['foo'])
