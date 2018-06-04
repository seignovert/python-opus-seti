# -*- coding: utf-8 -*-
import pytest
import responses
import six
import os

from opus.api import API
from opus.cli import read, data, metadata, image


@pytest.fixture
def api():
    return API('http://localhost/')

def test_read():
    assert read(['foo']) == {}
    assert read(['--foo']) == {}
    
    assert read(['--foo', 'bar']) == {'foo': 'bar'}
    assert read(['--foo=bar']) == {'foo': 'bar'}
    assert read(['--foo', '--bar']) == {}

    assert read(['--foo=bar', '123']) == {'foo': 'bar'}
    assert read(['--foo=123', '--bar', 'abc']) == {'foo': '123', 'bar': 'abc'}
    
    assert read(['--foo', '123', 'abc']) == {'foo': '123'}
    assert read(['--foo', '123', '--bar']) == {'foo': '123'}
    assert read(['--foo', '--bar', '123']) == {'bar': '123'}
    assert read(['123','--foo', '--bar']) == {}

    assert read(["--foo='bar'"]) == {'foo': 'bar'}
    assert read(["--foo='123 abc'"]) == {'foo': '123 abc'}
    assert read(["--foo", "'123 abc'"]) == {'foo': '123 abc'}

@responses.activate
def test_cli_data(api):
    json = open('tests/api/data.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=json)

    argv = ['--limit', '100']
    resp = data(argv, api=api)

    assert len(responses.calls) == 1
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/data.json?limit=100&page=1'
    else:
        assert 'limit=100' in responses.calls[0].request.url
        assert 'page=1' in responses.calls[0].request.url

    assert responses.calls[0].response.text == json
    assert len(resp) == 10

@responses.activate
def test_cli_data_limite_none(api):
    result_count = open('tests/api/meta/result_count.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/result_count.json',
                  body=result_count)

    json = open('tests/api/data_all.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=json)

    argv = ['--all', '--planet', 'Saturn']
    resp = data(argv, api=api)

    assert len(responses.calls) == 2
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn'
        assert responses.calls[1].request.url == 'http://localhost/data.json?planet=Saturn&limit=1591'
    else:
        assert 'limit=1591' in responses.calls[1].request.url

    assert responses.calls[1].response.text == json
    assert len(resp) == 1591


@responses.activate
def test_data_argv_none(api):
    responses.add(responses.GET, 'http://localhost/data.json',body='{}')
    argv = ['']
    with pytest.raises(SystemExit):
        resp = data(argv, api=api)
    assert len(responses.calls) == 0


@responses.activate
def test_cli_metadata(api):
    json = open('tests/api/metadata/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/metadata/S_IMG_CO_ISS_1459551972_N.json',
                   body=json)

    argv = ['S_IMG_CO_ISS_1459551972_N']
    resp = metadata(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/metadata/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == json

    assert resp.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'


@responses.activate
def test_cli_image(api):
    img = open('tests/api/image/med/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json',
                  body=img)

    argv = ['S_IMG_CO_ISS_1459551972_N', '--size', 'med']
    resp = image(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == img

    assert resp == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'


@responses.activate
def test_cli_image_download(api):
    fname = 'N1459551972_1_med.jpg'
    jpg = 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

    img = open('tests/api/image/med/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json',
                  body=img)

    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, jpg,
                      body=img.read(), status=200,
                      content_type='image/jpeg',
                      stream=True
                      )

    argv = ['S_IMG_CO_ISS_1459551972_N', '--output', 'tests/test.jpg']
    resp = image(argv, api=api)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[1].request.url == jpg

    assert resp == 'tests/test.jpg'
    assert os.path.isfile('tests/test.jpg')
    os.remove('tests/test.jpg')
