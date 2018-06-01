# -*- coding: utf-8 -*-
import pytest
import responses
import six

from opus.api import API
from opus.cli import read, data, vims


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
def test_cli_vims(api):
    json = open('tests/api/data_vims.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=json)

    argv = ['TITAN']
    resp = vims(argv, api=api)

    assert len(responses.calls) == 1
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/data.json?surfacegeometrytargetname=TITAN&cols=ringobsid,target,revno,time1,primaryfilespec,channel&instrumentid=Cassini+VIMS&typeid=Image,Cube&limit=10&page=1'
    else:
        assert 'surfacegeometrytargetname=TITAN' in responses.calls[0].request.url

    assert responses.calls[0].response.text == json
    assert len(resp) == 10
