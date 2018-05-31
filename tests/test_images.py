# -*- coding: utf-8 -*-
import pytest
import os
import responses
import json as JSON

from opus.images import Images, Image

@pytest.fixture
def size():
    return 'med'

@pytest.fixture
def images(size):
    json = JSON.loads(open('tests/api/images/{}.json'.format(size), 'r').read())
    return Images(json, size)

@pytest.fixture
def image(size):
    ring_obs_id = 'S_IMG_CO_ISS_1459551972_N'
    json = JSON.loads(open('tests/api/image/'+size+'/'+ring_obs_id+'.json', 'r').read())
    return Image(ring_obs_id, json['path'], json['data'][0]['img'])

def test_images_meta(images, size):
    r = repr(images)
    assert 'OPUS API Images object' in r
    assert 'S_IMG_CO_ISS_1508094647_N' in r
    assert len(images) == 10
    assert images.order == 'obs_general.time1'
    assert images.size == size
    assert isinstance(images['S_IMG_CO_ISS_1508094647_N'], Image)

def test_images_image(image):
    assert repr(image) == 'OPUS API Image object: S_IMG_CO_ISS_1459551972_N'
    assert str(image) == 'S_IMG_CO_ISS_1459551972_N'
    assert image.ring_obs_id == 'S_IMG_CO_ISS_1459551972_N'
    assert image.path == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/'
    assert image.img == 'COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'
    assert image.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

def test_images_iter(images):
    for key in images:
        assert key in images.keys()
        break
    for value in images.values():
        assert isinstance(value, Image)
        break


@responses.activate
def test_image_download(image):
    fname = os.path.basename(image.url)

    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, image.url,
                    body=img.read(), status=200,
                    content_type='image/jpeg',
                    stream=True
        )

    image.download(out='tests/')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

    assert os.path.isfile('tests/'+fname)
    os.remove('tests/'+fname)


@responses.activate
def test_image_download_output(image):
    fname = os.path.basename(image.url)

    with open('tests/api/image/med/'+fname, 'rb') as img:
        responses.add(responses.GET, image.url,
                      body=img.read(), status=200,
                      content_type='image/jpeg',
                      stream=True
                      )

    image.download(out='tests/test.jpg')

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2001/data/1459551663_1459568594/N1459551972_1_med.jpg'

    assert os.path.isfile('tests/test.jpg')
    os.remove('tests/test.jpg')
