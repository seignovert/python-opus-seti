# -*- coding: utf-8 -*-
import pytest

from opus.api import API

@pytest.fixture
def url():
    return 'http://127.0.0.1:8000/'

@pytest.fixture
def api(url):
    return API(url)

def test_api_url(url):
    api = API(url)
    assert str(api) == url
    assert isinstance(repr(api), str)

def test_request_params(api):
    url = api.request('data', planet='Saturn', target='pan')
    assert url == api.url + 'data.json?planet=Saturn&target=pan'

def test_request_fmt(api):
    url = api.request('data', fmt='csv')
    assert url == api.url + 'data.csv'

def test_request_fmt_err(api):
    with pytest.raises(ValueError):
        api.request('data', fmt='txt')

def test_count(api):
    assert api.count(planet='Saturn', target='pan') == 1591

# def test_data(api):
#     data = api.data(limit=1, page=2, target='pan')
#     assert data['Ring Observation ID'] == 'S_IMG_CO_ISS_1488190255_N'
