# -*- coding: utf-8 -*-
import pytest
import os
import responses
import json as JSON

from opus.images import *

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
    assert repr(images) == 'OPUS API Images object (with 10 images)'
    assert len(images) == 10
    assert images.order == 'obs_general.time1'
    assert images.size == size


def test_images_image(images):
    image = images[0]
    assert repr(image) == 'OPUS API Image object: S_IMG_CO_ISS_1508094647_N'
    assert str(image) == 'S_IMG_CO_ISS_1508094647_N'
    assert image.ring_obs_id == 'S_IMG_CO_ISS_1508094647_N'
    assert image.path == 'https://pds-rings.seti.org/holdings/previews/'
    assert image.img == 'COISS_2xxx/COISS_2016/data/1508054834_1508117267/N1508094647_1_med.jpg'
    assert image.url == 'https://pds-rings.seti.org/holdings/previews/COISS_2xxx/COISS_2016/data/1508054834_1508117267/N1508094647_1_med.jpg'
    

def test_images_iter(images):
    images.next() == images[0]
    for ii, img in enumerate(images):
        img = images[ii]


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
