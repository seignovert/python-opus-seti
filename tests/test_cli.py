# -*- coding: utf-8 -*-
import pytest
import responses
import six
import os

from opus.api import API
import opus.cli as cli


@pytest.fixture
def api():
    return API('http://localhost/')

def test_read():
    assert cli.read('foo'.split()) == {}
    assert cli.read('--foo'.split()) == {}
    
    assert cli.read('--foo bar'.split()) == {'foo': 'bar'}
    assert cli.read('--foo=bar'.split()) == {'foo': 'bar'}
    assert cli.read('--foo --bar'.split()) == {}

    assert cli.read('--foo=bar 123'.split()) == {'foo': 'bar'}
    assert cli.read('--foo=123 --bar abc'.split()) == {'foo': '123', 'bar': 'abc'}
    
    assert cli.read('--foo 123 abc'.split()) == {'foo': '123'}
    assert cli.read('--foo 123 --bar'.split()) == {'foo': '123'}
    assert cli.read('--foo --bar 123'.split()) == {'bar': '123'}
    assert cli.read('123 --foo --bar'.split()) == {}

    assert cli.read("--foo='bar'".split()) == {'foo': 'bar'}
    assert cli.read(["--foo='123 abc'"]) == {'foo': '123 abc'}
    assert cli.read(["--foo", "'123 abc'"]) == {'foo': '123 abc'}

@responses.activate
def test_cli_data(api):
    json = open('tests/api/data.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=json)

    argv = '--limit 100'.split()
    resp = cli.data(argv, api=api)

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

    argv = '--all --planet Saturn'.split()
    resp = cli.data(argv, api=api)

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
        resp = cli.data(argv, api=api)
    assert len(responses.calls) == 0


@responses.activate
def test_cli_metadata(api):
    json = open('tests/api/metadata/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/metadata/S_IMG_CO_ISS_1459551972_N.json',
                   body=json)

    argv = 'S_IMG_CO_ISS_1459551972_N'.split()
    resp = cli.metadata(argv, api=api)

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

    argv = 'S_IMG_CO_ISS_1459551972_N --size med'.split()
    resp = cli.image(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == img

    assert resp == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'


@responses.activate
def test_cli_image_download(api):
    img = open('tests/api/image/med/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json',
                  body=img)

    fname = 'N1459551972_1_med.jpg'
    jpg = 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, jpg,
                      body=img.read(), status=200,
                      content_type='image/jpeg',
                      stream=True
                      )

    argv = 'S_IMG_CO_ISS_1459551972_N --output tests/test.jpg'.split()
    resp = cli.image(argv, api=api)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[1].request.url == jpg

    assert resp == 'tests/test.jpg'
    assert os.path.isfile('tests/test.jpg')
    os.remove('tests/test.jpg')


@responses.activate
def test_cli_files(api):
    json = open('tests/api/files/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json',
                  body=json)

    argv = 'S_IMG_CO_ISS_1459551972_N'.split()
    resp = cli.files(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == json

    assert 'OPUS API Files for observation: S_IMG_CO_ISS_1459551972_N' in resp
    assert 'LBL: https://pds-rings.seti.org/holdings/calibrated/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_CALIB.LBL' in resp


@responses.activate
def test_cli_files_downlad(api):
    json = open('tests/api/files/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json',
                  body=json)

    fname = 'N1459551972_1.LBL'
    lbl = 'https://pds-rings.seti.org/holdings/volumes/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1.LBL'

    with open('tests/data/'+fname, 'rb') as img:
        responses.add(responses.GET, lbl,
                      body=img.read(), status=200,
                      content_type='image/txt',
                      stream=True
                      )

    argv = 'S_IMG_CO_ISS_1459551972_N -f RAW_IMAGE LBL --output tests/test.lbl'.split()
    resp = cli.files(argv, api=api)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[1].request.url == lbl

    assert resp == 'tests/test.lbl'
    assert os.path.isfile('tests/test.lbl')
    os.remove('tests/test.lbl')


@responses.activate
def test_cli_field(api):
    json = open('tests/api/fields/target.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields/target.json',
                  body=json)

    argv = 'target'.split()
    resp = cli.field(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/fields/target.json'
    assert responses.calls[0].response.text == json

    assert resp.label == 'Intended Target Name'


@responses.activate
def test_cli_field_all(api):
    json = open('tests/api/fields.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields.json',
                  body=json)

    argv = '--all'.split()
    resp = cli.field(argv, api=api)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/fields.json'
    assert responses.calls[0].response.text == json

    r = repr(resp)
    assert 'OPUS API list of all fields available (304):' in r
    assert 'GLOBAL' in r
    assert 'TITAN' in r

@responses.activate
def test_cli_field_group(api):
    json = open('tests/api/fields.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields/TITAN.json',
                  body='{}')
    responses.add(responses.GET,
                  'http://localhost/fields.json',
                  body=json)

    argv = 'TITAN'.split()
    resp = cli.field(argv, api=api)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/fields/TITAN.json'
    assert responses.calls[0].response.text == '{}'
    assert responses.calls[1].request.url == 'http://localhost/fields.json'
    assert responses.calls[1].response.text == json

    r = repr(resp)
    assert 'OPUS API Surface Geometry fields (31) for `Titan`:' in r
    assert 'Sub-Solar IAU West Longitude (subsolarIAUlongitude)' in r

@responses.activate
def test_cli_field_err(api):
    json = open('tests/api/fields.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields/abc.json',
                  body='{}')
    responses.add(responses.GET,
                  'http://localhost/fields.json',
                  body=json)

    argv = 'abc'.split()
    resp = cli.field(argv, api=api)

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == 'http://localhost/fields/abc.json'
    assert responses.calls[0].response.text == '{}'
    assert responses.calls[1].request.url == 'http://localhost/fields.json'
    assert responses.calls[1].response.text == json

    assert resp == 'Unknown field. To list all the available fields, run: `opus-field --all`'
