# -*- coding: utf-8 -*-
import pytest
import responses

from opus.api import API

@pytest.fixture
def url():
    return 'http://localhost/'

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


@responses.activate
def test_load_err(url):
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  json={'error': 'not found'}, status=404)

    with pytest.raises(RuntimeError):
        API(url, verbose=True).load('data')

@responses.activate
def test_count(api):
    result_count = open('tests/api/meta/result_count.json', 'r').read()
    responses.add(responses.GET,
                   'http://localhost/meta/result_count.json',
                   body=result_count)

    resp = api.count(planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn&target=pan'
    assert responses.calls[0].response.text == result_count
    
    assert resp == 1591

@responses.activate
def test_data(api):
    result_count = open('tests/api/meta/result_count.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/result_count.json',
                  body=result_count)

    data = open('tests/api/data_all.json', 'r').read()
    responses.add(responses.GET,
                   'http://localhost/data.json',
                   body=data)

    resp = api.data(planet='Saturn', target='pan')

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn&target=pan'
    assert responses.calls[1].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=1591'
    assert responses.calls[1].response.text == data


@responses.activate
def test_data_limit(api):
    data = open('tests/api/data.json', 'r').read()
    responses.add(responses.GET,
                   'http://localhost/data.json',
                   body=data)

    resp = api.data(limit=10, page=2, planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=10&page=2'
    assert responses.calls[0].response.text == data
