# -*- coding: utf-8 -*-
import pytest
import responses
import six

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
    if six.PY3:
        assert url == api.url + 'data.json?planet=Saturn&target=pan'
    else:
        assert api.url in url
        assert 'data.json?' in url
        assert 'planet=Saturn' in url
        assert 'target=pan' in url


def test_api_request_fmt(api):
    url = api.request('data', fmt='csv')
    url = api.request('data', fmt='csv')
    assert url == api.url + 'data.csv'
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
    if six.PY3:
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
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn&target=pan'
        assert responses.calls[1].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=1591'
    else:
        assert 'limit=1591' in responses.calls[1].request.url
    assert responses.calls[1].response.text == data

    assert len(resp) == 1591 


@responses.activate
def test_api_data_limit(api):
    data = open('tests/api/data.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/data.json',
                  body=data)

    resp = api.data(limit=10, page=2, planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/data.json?planet=Saturn&target=pan&limit=10&page=2'
    else:
        assert 'limit=10' in responses.calls[0].request.url
        assert 'page=2' in responses.calls[0].request.url

    assert responses.calls[0].response.text == data

    assert len(resp) == 10

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

    assert resp.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'

@responses.activate
def test_api_images(api):
    result_count = open('tests/api/meta/result_count.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/result_count.json',
                  body=result_count)

    images = open('tests/api/images/med.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/images/med.json',
                  body=images)

    resp = api.images(size='med', planet='Saturn', target='pan')

    assert len(responses.calls) == 2
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn&target=pan'
        assert responses.calls[1].request.url == 'http://localhost/images/med.json?planet=Saturn&target=pan&limit=1591'
    assert responses.calls[1].response.text == images

@responses.activate
def test_api_images_limit(api):
    images = open('tests/api/images/med.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/images/med.json',
                  body=images)

    resp = api.images(size='med', limit=10, page=2, planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/images/med.json?planet=Saturn&target=pan&limit=10&page=2'
    assert responses.calls[0].response.text == images

    assert len(resp) == 10

@responses.activate
def test_api_image(api):
    image = open('tests/api/image/med/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json',
                   body=image)

    resp = api.image('S_IMG_CO_ISS_1459551972_N')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/image/med/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == image

    assert resp.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'


def test_api_images_size_err(api):
    with pytest.raises(ValueError):
        api.images('abc')


def test_api_image_size_err(api):
    with pytest.raises(ValueError):
        api.image('S_IMG_CO_ISS_1459551972_N', size='abc')


@responses.activate
def test_api_file(api):
    json = open(
        'tests/api/files/S_IMG_CO_ISS_1459551972_N.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json',
                  body=json)

    resp = api.file('S_IMG_CO_ISS_1459551972_N')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/files/S_IMG_CO_ISS_1459551972_N.json'
    assert responses.calls[0].response.text == json

    assert resp.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'


@responses.activate
def test_api_files(api):
    result_count = open('tests/api/meta/result_count.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/result_count.json',
                  body=result_count)

    files = open('tests/api/files.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/files.json',
                  body=files)

    resp = api.files(planet='Saturn', target='pan')

    assert len(responses.calls) == 2
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/meta/result_count.json?planet=Saturn&target=pan'
        assert responses.calls[1].request.url == 'http://localhost/files.json?planet=Saturn&target=pan&limit=1591'
    assert responses.calls[1].response.text == files


@responses.activate
def test_api_files_limit(api):
    files = open('tests/api/files.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/files.json',
                  body=files)

    resp = api.files(limit=10, page=2, planet='Saturn', target='pan')

    assert len(responses.calls) == 1
    if six.PY3:
        assert responses.calls[0].request.url == 'http://localhost/files.json?planet=Saturn&target=pan&limit=10&page=2'
    assert responses.calls[0].response.text == files

    assert len(resp) == 10

@responses.activate
def test_api_mults(api):
    mults = open('tests/api/meta/mults/target.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/mults/target.json',
                  body=mults)

    resp = api.mults('target', planet='Saturn')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/meta/mults/target.json?planet=Saturn'
    assert responses.calls[0].response.text == mults

    assert len(resp) == 63

@responses.activate
def test_api_range(api):
    range_endpoints = open('tests/api/meta/range/endpoints/ringradius1.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/meta/range/endpoints/ringradius1.json',
                  body=range_endpoints)

    resp = api.range('ringradius1', target='Saturn')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/meta/range/endpoints/ringradius1.json?target=Saturn'
    assert responses.calls[0].response.text == range_endpoints

    assert repr(resp) == 'OPUS API Range endpoints for field: ringradius1'
    assert resp.min == 60000
    assert resp.max == 1.29e+07
    assert resp.nulls == 115573


@responses.activate
def test_api_field(api):
    field = open('tests/api/fields/target.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields/target.json',
                  body=field)

    resp = api.field('target')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/fields/target.json'
    assert responses.calls[0].response.text == field

    assert resp.label == 'Intended Target Name'

@responses.activate
def test_api_fields(api):
    fields = open('tests/api/fields.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/fields.json',
                  body=fields)

    resp = api.fields()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/fields.json'
    assert responses.calls[0].response.text == fields

    assert len(resp) == 3971


@responses.activate
def test_api_category(api):
    category = open('tests/api/category/obs_general.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/category/obs_general.json',
                  body=category)

    resp = api.category('obs_general')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/category/obs_general.json'
    assert responses.calls[0].response.text == category

    assert resp.name == 'obs_general'


@responses.activate
def test_api_categories(api):
    categories = open('tests/api/categories.json', 'r').read()
    responses.add(responses.GET,
                  'http://localhost/categories.json',
                  body=categories)

    resp = api.categories()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost/categories.json'
    assert responses.calls[0].response.text == categories

    assert len(resp) == 3
