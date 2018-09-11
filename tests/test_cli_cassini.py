# -*- coding: utf-8 -*-
import pytest
import responses
import six

from opus.api import API
from opus.cli.cassini import vims


@pytest.fixture
def api():
    return API('http://localhost/')


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
        assert responses.calls[0].request.url == 'http://localhost/data.json?target=TITAN&cols=opusid,target,revno,time1,primaryfilespec&instrumentid=Cassini+VIMS&COVIMSswathlength1=2&COVIMSswathwidth1=2&limit=10&page=1'
    else:
        assert 'surfacegeometrytargetname=TITAN' in responses.calls[0].request.url

    assert responses.calls[0].response.text == json
    assert len(resp) == 10
