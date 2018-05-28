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


def test_api_request_params(api):
    url = api.request('data', planet='Saturn', target='pan')
    assert url == api.url + 'data.json?planet=Saturn&target=pan'


def test_api_request_fmt(api):
    url = api.request('data', fmt='csv')
    assert url == api.url + 'data.csv'


def test_api_request_fmt_err(api):
    with pytest.raises(ValueError):
        api.request('data', fmt='txt')


@responses.activate
def test_api_load_err(url):
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  json={'error': 'not found'}, status=404)

    with pytest.raises(RuntimeError):
        API(url, verbose=True).load('data')

@responses.activate
def test_api_count(api):
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
def test_api_data(api):
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
    assert (responses.calls[1].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=1591') \
        or (responses.calls[1].request.url == 'http://localhost/data.json?planet=Saturn&limit=1591&target=pan') # Python < 3.6 (Not ordered kwargs)
    assert responses.calls[1].response.text == data


@responses.activate
def test_api_data_limit(api):
    data = open('tests/api/data.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=data)

    resp = api.data(limit=10, page=2, planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    assert (responses.calls[0].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=10&page=2') \
        or (responses.calls[0].request.url == 'http://localhost/data.json?planet=Saturn&limit=10&target=pan&page=2')
    assert responses.calls[0].response.text == data


@responses.activate
def test_api_metadata(api):
    metadata = open('tests/api/metadata/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/metadata/S_IMG_CO_ISS_1459551972_N.json',
                   body=metadata)

    resp = api.metadata('S_IMG_CO_ISS_1459551972_N')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/metadata/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == metadata
