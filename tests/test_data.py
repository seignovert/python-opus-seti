# -*- coding: utf-8 -*-
import pytest

import json as JSON

from opus.data import Data

@pytest.fixture
def json():
    return JSON.loads(open('tests/api/data.json', 'r').read())

@pytest.fixture
def data(json):
    return Data(json)

def test_data_meta(data):
    assert repr(data) == 'OPUS API Data object (with 10 elements)'
    assert len(data) == 10
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


def test_data_images(data):
    img = data[0]
    assert img[0] == 'S_IMG_CO_ISS_1508094647_N'
    assert img[1] == 'SAT'
    assert img[2] == 'PAN'
    assert img[3] == 87.786
    assert img[4] == 88.169
    assert img[5] == '2005-288T18:42:08.622'
    assert img[6] == '2005-288T18:42:09.302'


def test_data_iter(data):
    data.next() == data[0]
    for ii, img in enumerate(data):
        img = data[ii]
